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
                const t = document.getElementById('chat-input')
                t.value = ''
                t.style.height = 'auto'
                t.style.height = t.scrollHeight + 'px'
                const button = document.getElementById('chat-button')
                button.style.display = 'none'
                unlocked.onClear()
            }
            function onChange(event, newValue) {
                const t = event.target
                if (newValue !== undefined) t.value = newValue
                const chat = document.getElementById('chat')
                const wasAtBottom = getIsAtBottom(chat)
                t.style.height = 'auto'
                t.style.height = t.scrollHeight + 'px'
                const button = document.getElementById('chat-button')
                if (t.value === '') button.style.display = 'none'
                else button.style.display = 'unset'
                unlocked.onInputChange(t.value)
                if (wasAtBottom) scrollToBottom(chat)
            }
            setHooks({
                onClear,
                onChange,
                onKeyDown: function(event) {
                    if (event.ctrlKey && event.key === 'Enter') {
                        onClear(event)
                    }
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
            <button id="chat-button"
                    className={styles.button}
                    style={{display: "none"}}
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
    return <textarea
               id="chat-input"
               ref={inpRef}
               name="message"
               placeholder="Stream typing"
               rows="1"
               className={styles.input}
               value={inputValue}
               onChange={onChange}
               onKeyDown={onKeyDown}
           />
}
