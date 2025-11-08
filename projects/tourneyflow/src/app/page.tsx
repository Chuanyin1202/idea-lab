import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          {/* Hero Section */}
          <div className="mb-16">
            <h1 className="text-6xl font-bold text-white mb-6">
              TourneyFlow
            </h1>
            <p className="text-2xl text-purple-200 mb-8">
              為電競賽事主辦方打造的一站式管理平台
            </p>
            <p className="text-lg text-slate-300 max-w-2xl mx-auto mb-12">
              自動產生對戰表、更新晉級結果，10 分鐘快速建立專業賽事
            </p>

            {/* CTA Button */}
            <Link
              href="/create"
              className="inline-block bg-purple-600 hover:bg-purple-700 text-white font-bold text-lg px-8 py-4 rounded-lg transition-all transform hover:scale-105 shadow-lg hover:shadow-xl"
            >
              🚀 立即建立賽事
            </Link>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-2 gap-8 mb-16">
            <FeatureCard
              icon="⚡"
              title="10 分鐘建立賽事"
              description="填寫基本資訊，系統自動產生對戰表"
            />
            <FeatureCard
              icon="🎯"
              title="一鍵更新結果"
              description="後台輸入比分，自動計算晉級名單"
            />
            <FeatureCard
              icon="🏆"
              title="單/雙淘汰賽制"
              description="支援多種常見賽制，自動排程"
            />
            <FeatureCard
              icon="🎨"
              title="美觀對戰表"
              description="專業的視覺化對戰樹狀圖"
            />
          </div>

          {/* Demo Section */}
          <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-8 mb-8">
            <h3 className="text-2xl font-bold text-white mb-4">MVP 功能展示</h3>
            <div className="text-left text-slate-300 space-y-2">
              <div className="flex items-center gap-3">
                <span className="text-green-400">✓</span>
                <span>賽事建立表單</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-green-400">✓</span>
                <span>單淘汰賽對戰表自動生成</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-green-400">✓</span>
                <span>比賽結果更新與晉級計算</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-green-400">✓</span>
                <span>即時對戰表視覺化</span>
              </div>
            </div>
          </div>

          {/* Tech Stack */}
          <div className="mt-16 pt-16 border-t border-slate-700">
            <p className="text-slate-400 text-sm mb-4">Powered by</p>
            <div className="flex justify-center gap-6 text-slate-500">
              <TechBadge name="Next.js 14" />
              <TechBadge name="TypeScript" />
              <TechBadge name="Tailwind CSS" />
              <TechBadge name="Vercel" />
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}

function FeatureCard({ icon, title, description }: { icon: string; title: string; description: string }) {
  return (
    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-slate-300">{description}</p>
    </div>
  )
}

function TechBadge({ name }: { name: string }) {
  return (
    <span className="text-sm font-mono">{name}</span>
  )
}
