import UriHome from '../mod/UriHome.js'
import uriFirstArg from '../mod/uriFirstArg.js'
import RoomList from '../components/roomList.jsx'
import Layout from '../components/layout.jsx'
import styles from '../components/styles.module.css'
import { useEffect, useState } from "react"

export default function Home({env}) {
    const [rooms, setRooms] = useState(null)
    const uri = new UriHome(env.home)
    useEffect(function() {
        getRooms(uri, setRooms)
    }, [])
    return Layout({env, styles, children: RoomList({rooms, styles})})
}

function getRooms(uri, setRooms) {
    const with200 = fetch(uri.rooms()).then(function(res) {
        if (res.status !== 200) {
            setRooms("error")
            throw new Error("couldn't fetch " + uri.rooms())
        }
        return res.json()
    })
    with200.catch(function(err) {
        console.error("can't JSON parse response of " + uri.rooms())
        throw err
    })
    const withJson = with200.then(
        json => json.map(e => ({
            text: e.name || '<unnamed>',
            href: uri.room(e.id)
        })))

    withJson.then(setRooms)
}

export async function getStaticProps() {
    return {props: {env: uriFirstArg}}
}
