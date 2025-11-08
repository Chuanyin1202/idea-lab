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
            <p className="text-lg text-slate-300 max-w-2xl mx-auto">
              自動產生對戰表、更新晉級結果，並透過 Discord / Email 自動通知選手與工作人員
            </p>
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
              icon="🔔"
              title="自動通知"
              description="Discord Bot / Email 自動通知選手"
            />
            <FeatureCard
              icon="🎨"
              title="公開賽事頁"
              description="美觀的賽事頁面，支援嵌入 Twitch 直播"
            />
          </div>

          {/* Status Badge */}
          <div className="inline-block bg-green-500/20 border border-green-500/50 rounded-full px-6 py-3 mb-4">
            <p className="text-green-200 font-medium">
              ✅ 已部署 - 自動化測試中
            </p>
          </div>
          <p className="text-sm text-slate-400 mt-4">
            每次 push 程式碼都會自動部署到 Vercel 🚀
          </p>

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
