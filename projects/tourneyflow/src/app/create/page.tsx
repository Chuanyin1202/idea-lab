'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function CreateTournament() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    name: '',
    game: '',
    date: '',
    teamCount: 8,
    format: 'single-elimination'
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // 生成唯一 ID
    const tournamentId = `tournament-${Date.now()}`

    // 儲存到 localStorage
    const tournament = {
      id: tournamentId,
      ...formData,
      createdAt: new Date().toISOString(),
      matches: []
    }

    localStorage.setItem(tournamentId, JSON.stringify(tournament))

    // 導向對戰表頁面
    router.push(`/tournament/${tournamentId}`)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <Link
              href="/"
              className="text-purple-300 hover:text-purple-200 mb-4 inline-block"
            >
              ← 返回首頁
            </Link>
            <h1 className="text-4xl font-bold text-white mb-2">建立新賽事</h1>
            <p className="text-slate-300">填寫基本資訊，系統將自動產生對戰表</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-8">
            {/* Tournament Name */}
            <div className="mb-6">
              <label className="block text-white font-semibold mb-2">
                賽事名稱 <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-purple-500"
                placeholder="例：2025 春季盃"
              />
            </div>

            {/* Game */}
            <div className="mb-6">
              <label className="block text-white font-semibold mb-2">
                遊戲類型 <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                required
                value={formData.game}
                onChange={(e) => setFormData({ ...formData, game: e.target.value })}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-purple-500"
                placeholder="例：League of Legends, Valorant"
              />
            </div>

            {/* Date */}
            <div className="mb-6">
              <label className="block text-white font-semibold mb-2">
                賽事日期 <span className="text-red-400">*</span>
              </label>
              <input
                type="date"
                required
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white focus:outline-none focus:border-purple-500"
              />
            </div>

            {/* Team Count */}
            <div className="mb-6">
              <label className="block text-white font-semibold mb-2">
                隊伍數量 <span className="text-red-400">*</span>
              </label>
              <select
                value={formData.teamCount}
                onChange={(e) => setFormData({ ...formData, teamCount: parseInt(e.target.value) })}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white focus:outline-none focus:border-purple-500"
              >
                <option value={4}>4 隊</option>
                <option value={8}>8 隊</option>
                <option value={16}>16 隊</option>
                <option value={32}>32 隊</option>
              </select>
              <p className="text-slate-400 text-sm mt-2">
                對戰表將根據隊伍數量自動生成
              </p>
            </div>

            {/* Format */}
            <div className="mb-8">
              <label className="block text-white font-semibold mb-2">
                賽制 <span className="text-red-400">*</span>
              </label>
              <select
                value={formData.format}
                onChange={(e) => setFormData({ ...formData, format: e.target.value })}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white focus:outline-none focus:border-purple-500"
              >
                <option value="single-elimination">單淘汰賽</option>
                <option value="double-elimination" disabled>雙淘汰賽（即將推出）</option>
              </select>
              <p className="text-slate-400 text-sm mt-2">
                MVP 版本僅支援單淘汰賽制
              </p>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-4 rounded-lg transition-all transform hover:scale-105 shadow-lg"
            >
              🚀 建立賽事並生成對戰表
            </button>
          </form>

          {/* Info Box */}
          <div className="mt-8 bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
            <p className="text-blue-200 text-sm">
              💡 提示：賽事建立後，您可以輸入隊伍名稱並更新比賽結果。對戰表會即時更新晉級狀況。
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
