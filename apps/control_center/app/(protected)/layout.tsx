import { redirect } from "next/navigation";
import { hasSession } from "@/lib/session";
import { Nav } from "@/components/Nav";
export default async function Protected({children}:{children:React.ReactNode}){if(!(await hasSession()))redirect("/login");return <div className="shell"><Nav/><main className="main">{children}</main></div>}
