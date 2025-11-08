// 單淘汰賽對戰表生成算法

export interface Team {
  id: string
  name: string
}

export interface Match {
  id: string
  round: number
  matchNumber: number
  team1?: Team
  team2?: Team
  winner?: Team
  score1?: number
  score2?: number
}

export interface Tournament {
  id: string
  name: string
  game: string
  date: string
  teamCount: number
  format: string
  teams: Team[]
  matches: Match[]
  createdAt: string
}

/**
 * 生成單淘汰賽對戰表
 */
export function generateSingleEliminationBracket(teamCount: number): Match[] {
  const matches: Match[] = []
  const rounds = Math.log2(teamCount)

  let matchId = 1

  // 生成每一輪的對戰
  for (let round = 1; round <= rounds; round++) {
    const matchesInRound = teamCount / Math.pow(2, round)

    for (let i = 0; i < matchesInRound; i++) {
      matches.push({
        id: `match-${matchId}`,
        round,
        matchNumber: i + 1,
        team1: undefined,
        team2: undefined,
        winner: undefined,
        score1: undefined,
        score2: undefined
      })
      matchId++
    }
  }

  return matches
}

/**
 * 將隊伍填入對戰表的第一輪
 */
export function seedTeams(matches: Match[], teams: Team[]): Match[] {
  const firstRoundMatches = matches.filter(m => m.round === 1)

  firstRoundMatches.forEach((match, index) => {
    const team1Index = index * 2
    const team2Index = index * 2 + 1

    if (teams[team1Index]) {
      match.team1 = teams[team1Index]
    }
    if (teams[team2Index]) {
      match.team2 = teams[team2Index]
    }
  })

  return matches
}

/**
 * 更新比賽結果並自動晉級
 */
export function updateMatchResult(
  matches: Match[],
  matchId: string,
  score1: number,
  score2: number
): Match[] {
  const matchIndex = matches.findIndex(m => m.id === matchId)
  if (matchIndex === -1) return matches

  const match = matches[matchIndex]
  match.score1 = score1
  match.score2 = score2

  // 判定勝者
  if (score1 > score2 && match.team1) {
    match.winner = match.team1
  } else if (score2 > score1 && match.team2) {
    match.winner = match.team2
  }

  // 自動晉級到下一輪
  if (match.winner) {
    const nextRound = match.round + 1
    const nextMatchNumber = Math.ceil(match.matchNumber / 2)

    const nextMatch = matches.find(
      m => m.round === nextRound && m.matchNumber === nextMatchNumber
    )

    if (nextMatch) {
      // 決定勝者進入下一場的哪一邊
      if (match.matchNumber % 2 === 1) {
        nextMatch.team1 = match.winner
      } else {
        nextMatch.team2 = match.winner
      }
    }
  }

  return [...matches]
}

/**
 * 取得輪次名稱
 */
export function getRoundName(round: number, totalRounds: number): string {
  if (round === totalRounds) return '決賽'
  if (round === totalRounds - 1) return '準決賽'
  if (round === totalRounds - 2) return '八強'
  if (round === totalRounds - 3) return '十六強'
  return `第 ${round} 輪`
}

/**
 * 計算總輪數
 */
export function getTotalRounds(teamCount: number): number {
  return Math.log2(teamCount)
}
