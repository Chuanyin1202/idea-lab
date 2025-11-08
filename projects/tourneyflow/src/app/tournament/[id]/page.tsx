'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import {
  Tournament,
  Team,
  Match,
  generateSingleEliminationBracket,
  seedTeams,
  updateMatchResult,
  getRoundName,
  getTotalRounds
} from '@/lib/bracket'

export default function TournamentPage() {
  const params = useParams()
  const router = useRouter()
  const tournamentId = params.id as string

  const [tournament, setTournament] = useState<Tournament | null>(null)
  const [teams, setTeams] = useState<Team[]>([])
  const [matches, setMatches] = useState<Match[]>([])
  const [isEditingTeams, setIsEditingTeams] = useState(true)
  const [selectedMatch, setSelectedMatch] = useState<Match | null>(null)

  // 載入賽事資料
  useEffect(() => {
    const stored = localStorage.getItem(tournamentId)
    if (!stored) {
      router.push('/')
      return
    }

    const data: Tournament = JSON.parse(stored)
    setTournament(data)

    // 如果已有隊伍和對戰表，直接載入
    if (data.teams && data.teams.length > 0) {
      setTeams(data.teams)
      setIsEditingTeams(false)
    } else {
      // 初始化空白隊伍
      const emptyTeams: Team[] = []
      for (let i = 0; i < data.teamCount; i++) {
        emptyTeams.push({
          id: `team-${i + 1}`,
          name: ''
        })
      }
      setTeams(emptyTeams)
    }

    if (data.matches && data.matches.length > 0) {
      setMatches(data.matches)
    }
  }, [tournamentId, router])

  // 儲存資料到 localStorage
  const saveTournament = (updatedMatches: Match[], updatedTeams: Team[]) => {
    if (!tournament) return

    const updated: Tournament = {
      ...tournament,
      teams: updatedTeams,
      matches: updatedMatches
    }

    localStorage.setItem(tournamentId, JSON.stringify(updated))
    setTournament(updated)
    setMatches(updatedMatches)
    setTeams(updatedTeams)
  }

  // 生成對戰表
  const handleGenerateBracket = () => {
    if (!tournament) return

    // 檢查是否所有隊伍都有名稱
    const allTeamsFilled = teams.every(t => t.name.trim() !== '')
    if (!allTeamsFilled) {
      alert('請填寫所有隊伍名稱')
      return
    }

    // 生成對戰表
    let bracket = generateSingleEliminationBracket(tournament.teamCount)
    bracket = seedTeams(bracket, teams)

    saveTournament(bracket, teams)
    setIsEditingTeams(false)
  }

  // 更新隊伍名稱
  const handleTeamNameChange = (index: number, name: string) => {
    const updated = [...teams]
    updated[index].name = name
    setTeams(updated)
  }

  // 更新比賽結果
  const handleUpdateScore = (matchId: string, score1: number, score2: number) => {
    const updatedMatches = updateMatchResult(matches, matchId, score1, score2)
    saveTournament(updatedMatches, teams)
    setSelectedMatch(null)
  }

  if (!tournament) {
    return <div className="min-h-screen bg-slate-900 flex items-center justify-center text-white">載入中...</div>
  }

  const totalRounds = getTotalRounds(tournament.teamCount)

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <Link href="/" className="text-purple-300 hover:text-purple-200 mb-4 inline-block">
            ← 返回首頁
          </Link>
          <h1 className="text-4xl font-bold text-white mb-2">{tournament.name}</h1>
          <div className="flex gap-4 text-slate-300">
            <span>🎮 {tournament.game}</span>
            <span>📅 {tournament.date}</span>
            <span>👥 {tournament.teamCount} 隊</span>
          </div>
        </div>

        {/* Team Input Section */}
        {isEditingTeams && (
          <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-8 mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">輸入隊伍名稱</h2>
            <div className="grid md:grid-cols-2 gap-4 mb-6">
              {teams.map((team, index) => (
                <div key={team.id}>
                  <label className="block text-white mb-2">隊伍 {index + 1}</label>
                  <input
                    type="text"
                    value={team.name}
                    onChange={(e) => handleTeamNameChange(index, e.target.value)}
                    className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-purple-500"
                    placeholder={`輸入隊伍 ${index + 1} 名稱`}
                  />
                </div>
              ))}
            </div>
            <button
              onClick={handleGenerateBracket}
              className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 rounded-lg transition-all"
            >
              ✨ 生成對戰表
            </button>
          </div>
        )}

        {/* Bracket Display */}
        {!isEditingTeams && matches.length > 0 && (
          <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-8">
            <h2 className="text-2xl font-bold text-white mb-6">對戰表</h2>

            <div className="overflow-x-auto">
              <div className="flex gap-8 min-w-max">
                {Array.from({ length: totalRounds }, (_, roundIndex) => {
                  const round = roundIndex + 1
                  const roundMatches = matches.filter(m => m.round === round)

                  return (
                    <div key={round} className="flex-shrink-0" style={{ width: '300px' }}>
                      <h3 className="text-lg font-bold text-purple-300 mb-4 text-center">
                        {getRoundName(round, totalRounds)}
                      </h3>
                      <div className="space-y-4">
                        {roundMatches.map((match) => (
                          <div
                            key={match.id}
                            className="bg-white/5 border border-white/20 rounded-lg p-4 hover:bg-white/10 transition-all cursor-pointer"
                            onClick={() => setSelectedMatch(match)}
                          >
                            <div className="space-y-2">
                              {/* Team 1 */}
                              <div className={`flex justify-between items-center p-2 rounded ${
                                match.winner?.id === match.team1?.id ? 'bg-green-500/20' : ''
                              }`}>
                                <span className="text-white">
                                  {match.team1?.name || 'TBD'}
                                </span>
                                {match.score1 !== undefined && (
                                  <span className="text-white font-bold">{match.score1}</span>
                                )}
                              </div>

                              {/* VS */}
                              <div className="text-center text-slate-400 text-sm">VS</div>

                              {/* Team 2 */}
                              <div className={`flex justify-between items-center p-2 rounded ${
                                match.winner?.id === match.team2?.id ? 'bg-green-500/20' : ''
                              }`}>
                                <span className="text-white">
                                  {match.team2?.name || 'TBD'}
                                </span>
                                {match.score2 !== undefined && (
                                  <span className="text-white font-bold">{match.score2}</span>
                                )}
                              </div>
                            </div>

                            {match.team1 && match.team2 && !match.winner && (
                              <p className="text-xs text-purple-300 mt-2 text-center">
                                點擊輸入比分
                              </p>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        )}

        {/* Score Input Modal */}
        {selectedMatch && selectedMatch.team1 && selectedMatch.team2 && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <div className="bg-slate-800 rounded-xl p-6 max-w-md w-full">
              <h3 className="text-xl font-bold text-white mb-4">輸入比賽結果</h3>

              <div className="space-y-4 mb-6">
                <div>
                  <label className="block text-white mb-2">{selectedMatch.team1.name}</label>
                  <input
                    type="number"
                    min="0"
                    id="score1"
                    defaultValue={selectedMatch.score1 || 0}
                    className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg text-white focus:outline-none focus:border-purple-500"
                  />
                </div>

                <div>
                  <label className="block text-white mb-2">{selectedMatch.team2.name}</label>
                  <input
                    type="number"
                    min="0"
                    id="score2"
                    defaultValue={selectedMatch.score2 || 0}
                    className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg text-white focus:outline-none focus:border-purple-500"
                  />
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => setSelectedMatch(null)}
                  className="flex-1 bg-slate-600 hover:bg-slate-700 text-white font-bold py-2 rounded-lg"
                >
                  取消
                </button>
                <button
                  onClick={() => {
                    const score1 = parseInt((document.getElementById('score1') as HTMLInputElement).value)
                    const score2 = parseInt((document.getElementById('score2') as HTMLInputElement).value)
                    handleUpdateScore(selectedMatch.id, score1, score2)
                  }}
                  className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 rounded-lg"
                >
                  確認
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
