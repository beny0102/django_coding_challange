import MailLogTable from "@/components/MailLogTable"
//route all inside /pages


export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <div className="flex flex-col items-center justify-center mb-16 lg:mb-0 lg:items-start">
          
          <h1 className="text-5xl font-bold leading-tight tracking-tighter text-center lg:text-left lg:text-7xl">
            <span className="block">MailLog</span>
            <span className="block text-blue-600 dark:text-blue-400">A simple mail log</span>
          </h1>
          <p className="mt-5 text-center lg:text-left text-gray-500 dark:text-gray-400">
            the latest emails sent
          </p>
          <a className="mt-5 text-center lg:text-left text-gray-500 dark:text-gray-400" href="/licenses">Licenses</a>
        </div>
      </div>

      <MailLogTable/>

    </main>
  )
}