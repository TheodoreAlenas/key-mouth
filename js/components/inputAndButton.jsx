import colors from './colors.module.css'
import shapes from './shapes.module.css'
import { useEffect, useRef, useState } from "react"

export default function InputAndButton({o, className}) {
    const defaultHooks = {
        onClear: function(e) {e.preventDefault},
        onChange: function() {},
        onKeyDown: function() {}
    }
    const [hooks, setHooks] = useState(defaultHooks)
    if (o !== null) {
        o.onReadySocket = function(unlocked) {
            setHooks({
                onClear: function(event) {
                    event.preventDefault()
                    unlocked.onClear()
                },
                onChange: function(event) {
                    const t = event.target
                    t.style.height = 'auto'
                    t.style.height = t.scrollHeight + 'px'
                    unlocked.onInputChange(t.value)
                },
                onKeyDown: function(event) {
                    if (event.key !== 'Enter') return
                    if (getIsOnMobile()) {
                        event.preventDefault()
                        unlocked.onInputChange(event.target.value + '\n')
                        return
                    }
                    if (event.shiftKey) return
                    event.preventDefault()
                    unlocked.onClear()
                }
            })
        }
    }
    return (
        <form onSubmit={hooks.onClear}
              className={className + ' ' +
                         shapes.inputForm + ' ' +
                         colors.inputForm}>
            <Input o={o}
                   onChange={hooks.onChange}
                   onKeyDown={hooks.onKeyDown}
            />
            <button className={shapes.button + ' ' +
                               colors.button}
                    type="submit"
            >Clear</button>
        </form>
    )
}

function getIsOnMobile() {
    return / Android | webOS | iPhone | iPad | iPod | BlackBerry | IEMobile | Opera Mini /i.test(navigator.userAgent)
}

function Input({o, onChange, onKeyDown}) {
    const [inputValue, setInputValue] = useState('')
    if (o !== null) o.setInputValue = setInputValue
    const inpRef = useRef(null)
    useEffect(function() {
        const t = inpRef.current
        t.style.height = 'auto'
        t.style.height = t.scrollHeight + 'px'
    }, [])
    return (
        <div className={shapes.inputContainer + ' ' +
                        colors.inputContainer}>
            <textarea
                ref={inpRef}
                name="message"
                placeholder="Think and type"
                rows="1"
                className={shapes.input + ' ' +
                           colors.input}
                value={inputValue}
                onChange={onChange}
                onKeyDown={onKeyDown}
            />
        </div>
    )
}
