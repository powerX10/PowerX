export default function PageTitle({title,sub}:{title:string;sub?:string}){return <div className="pagetitle"><h1>{title}</h1>{sub&&<p>{sub}</p>}</div>}
