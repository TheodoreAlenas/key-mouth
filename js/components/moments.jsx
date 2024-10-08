import React, { useEffect, useRef, useState } from "react"
import { getIsAtBottom, scrollToBottom } from "./scrolling.js"
import Moment from './moment.jsx'

export default function Moments({o, styles}) {
    const [state, setState] = useState({
        atBottom: true,
        fromO: {moreTopButton: null, pages: [], moreBottomButton: null}
    })
    const ref = useRef(null)
    useEffect(function() {
        if (ref.current && state.atBottom) scrollToBottom(ref.current)
    }, [state])
    if (o === null || o === undefined) {
        return <code>{"Loading..."}</code>
    }
    o.onSocketError = function() {
        setState({atBottom: getIsAtBottom(ref.current), fromO: null})
    }
    o.setMoments = function(v) {
        setState({atBottom: getIsAtBottom(ref.current), fromO: v})
    }
    let finalPres = <code>{"ERROR"}</code>
    try {
        const pres = []
        const mt = state.fromO.moreTopButton
        if (state.fromO !== null && mt !== null) {
            pres.push(
                <button
                    key="moreTopButton"
                    onClick={mt.onClick}
                    className={styles.button + ' ' +
                               styles.moreTopButton}
                >{mt.label}</button>
            )
        }
        for (let page of state.fromO.pages) {
            for (let moment of page.moments) {
                pres.push(Moment({moment, styles}))
            }
        }
        const mb = state.fromO.moreBottomButton
        if (state.fromO !== null && mb !== null) {
            pres.push(
                <button
                    key="moreBottomButton"
                    onClick={mb.onClick}
                    className={styles.button + ' ' +
                               styles.moreBottomButton}
                >{mb.label}</button>
            )
        }
        finalPres = pres
    }
    catch (err) {
        console.error("couldn't present:")
        console.error(state.fromO)
        console.error(err)
    }
    return <section id="chat"
                    ref={ref}
                    className={styles.chat}
           >{finalPres}</section>
}
