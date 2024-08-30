import { useEffect, useRef, useState } from "react"
import { getIsAtBottom, scrollToBottom } from "./scrolling.js"

export default function InputAndButton({o, styles}) {
    const defaultHooks = {
        onClear: function(e) {e.preventDefault},
        onChange: function() {},
        onKeyDown: function() {}
    }
    const [hooks, setHooks] = useState(defaultHooks)
    if (o !== null) {
        o.onReadySocket = function(unlocked) {
            function onClear(event) {
                event.preventDefault()
                const t = event.target
                t.value = ''
                t.style.height = 'auto'
                t.style.height = t.scrollHeight + 'px'
                unlocked.onClear()
            }
            function onChange(event, newValue) {
                const t = event.target
                if (newValue !== undefined) t.value = newValue
                const chat = document.getElementById('chat')
                const wasAtBottom = getIsAtBottom(chat)
                t.style.height = 'auto'
                t.style.height = t.scrollHeight + 'px'
                unlocked.onInputChange(t.value)
                if (wasAtBottom) scrollToBottom(chat)
            }
            setHooks({
                onClear,
                onChange,
                onKeyDown: function(event) {
                    if (event.key !== 'Enter') return
                    if (getIsOnMobile()) {
                        onChange(event, event.target.value + '\n')
                        return
                    }
                    if (event.shiftKey) return
                    onClear(event)
                }
            })
        }
    }
    return (
        <form onSubmit={hooks.onClear}
              className={styles.inputForm}>
            <Input o={o}
                   styles={styles}
                   onChange={hooks.onChange}
                   onKeyDown={hooks.onKeyDown}
            />
            <button className={styles.button}
                    type="submit"
            >Clear</button>
        </form>
    )
}

function getIsOnMobile() {
    return / Android | webOS | iPhone | iPad | iPod | BlackBerry | IEMobile | Opera Mini /i.test(navigator.userAgent)
}

function Input({o, styles, onChange, onKeyDown}) {
    const [inputValue, setInputValue] = useState('')
    if (o !== null) o.setInputValue = setInputValue
    const inpRef = useRef(null)
    useEffect(function() {
        const t = inpRef.current
        t.style.height = 'auto'
        t.style.height = t.scrollHeight + 'px'
    }, [])
    return (
        <div className={styles.inputContainer}>
            <textarea
                ref={inpRef}
                name="message"
                placeholder="Stream typing"
                rows="1"
                className={styles.input}
                value={inputValue}
                onChange={onChange}
                onKeyDown={onKeyDown}
            />
        </div>
    )
}
