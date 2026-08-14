import Link from "next/link";
const links=[["Dashboard","/dashboard"],["Models","/models"],["Runtimes","/runtimes"],["Chat","/chat"],["Health","/health"],["Logs","/logs"],["Usage","/usage"],["Settings","/settings"]];
export function Nav(){return <><aside className="sidebar"><div className="brand"><div className="logo">X</div>PowerX</div><nav className="nav">{links.map(([n,h])=><Link key={h} href={h}>{n}</Link>)}</nav></aside><nav className="mobilebar">{links.slice(0,5).map(([n,h])=><Link key={h} href={h}>{n}</Link>)}</nav></>}
