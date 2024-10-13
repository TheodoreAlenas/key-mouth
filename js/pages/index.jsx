import IoHome from '../mod/io/IoHome.js'
import UriHome from '../mod/io/UriHome.js'
import uriFirstArg from '../mod/io/uriFirstArg.js'
import RoomList from '../components/roomList.jsx'
import Layout from '../components/layout.jsx'
import styles from '../components/styles.module.css'
import { useEffect, useState } from "react"

export default function Home({env}) {
    const [rooms, setRooms] = useState(null)
    const io = new IoHome({uri: new UriHome(env.home)})
    useEffect(function() {
        io.withRooms(setRooms)
    }, [])
    return Layout({env, styles, children: RoomList({rooms, styles})})
}

export async function getStaticProps() {
    return {props: {env: uriFirstArg}}
}
