import{redirect}from"next/navigation";import{hasSession}from"@/lib/session";import AppShell from"@/components/AppShell";import"@/app/fix-phase.css";
export default async function Layout({children}:{children:React.ReactNode}){if(!(await hasSession()))redirect("/login");return <AppShell>{children}</AppShell>}
