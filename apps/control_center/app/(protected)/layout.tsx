import{redirect}from"next/navigation";import{hasSession}from"@/lib/session";import AppShell from"@/components/AppShell";
export default async function Layout({children}:{children:React.ReactNode}){if(!(await hasSession()))redirect("/login");return <AppShell>{children}</AppShell>}
