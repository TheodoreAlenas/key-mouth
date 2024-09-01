import React, { useEffect, useRef, useState } from "react"
import { getIsAtBottom, scrollToBottom } from "./scrolling.js"
import Moment from './moment.jsx'

export default function Moments({o, styles}) {
    const [state, setState] = useState({atBottom: true, moments: []})
    const ref = useRef(null)
    useEffect(function() {
        if (ref.current && state.atBottom) scrollToBottom(ref.current)
    }, [state])
    if (o === null || o === undefined) {
        return <code>{"Loading..."}</code>
    }
    o.onSocketError = function() {
        setState({atBottom: getIsAtBottom(ref.current), moments: null})
    }
    o.setMoments = function(v) {
        setState({atBottom: getIsAtBottom(ref.current), moments: v})
    }
    let finalPres = <code>{"ERROR"}</code>
    try {
        const pres = state.moments.map(
            moment => Moment({moment, styles}))
        finalPres = pres
    }
    catch (err) {
        console.error("couldn't present:")
        console.error(state.moments)
        console.error(err)
    }
    return <section id="chat"
                    ref={ref}
                    className={styles.chat}
           >{finalPres}</section>
}
