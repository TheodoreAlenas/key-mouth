import UriHome from '../mod/UriHome.js'
import uriFirstArg from '../mod/uriFirstArg.js'
import RoomList from '../components/roomList.jsx'
import Layout from '../components/layout.jsx'
import { useEffect, useState } from "react"

export default function Home({env}) {
    const uri = new UriHome(env.home)
    const [rooms, setRooms] = useState(null)
    useEffect(function() {
        const with200 = fetch(uri.rooms()).then(function(res) {
            if (res.status !== 200) {
                setRooms(<code>ERROR</code>)
                throw new Error("couldn't fetch " + uri.rooms())
            }
            return res.json()
        })
        with200.catch(function(err) {
            console.error("can't JSON parse response of " + uri.rooms())
            throw err
        })
        with200.then(function(json) {
            setRooms(json.map(e => ({text: e, href: uri.room(e)})))
        })
    }, [])
    return <Layout env={env}><RoomList rooms={rooms} /></Layout>
}

export async function getStaticProps() {
    return {props: {env: uriFirstArg}}
}
