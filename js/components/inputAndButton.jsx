import styles from './inputAndButton.module.css'
import colors from './colors.module.css'
import { useEffect, useRef, useState } from "react"

export default function InputAndButton({o, className}) {
    const defaultHooks = {
        onSubmit: function(e) {e.preventDefault},
        onChange: function() {}
    }
    const [hooks, setHooks] = useState(defaultHooks)
    if (o !== null) {
        o.setOnReadySocket(function(unlocked) {
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
                }
            })
        })
    }
    return (
        <form onSubmit={hooks.onClear}
              className={className + ' ' +
                         styles.messengerInputForm + ' ' +
                         colors.inputForm}>
            <Input o={o} onChange={hooks.onChange} />
            <button className={styles.messengerButton + ' ' +
                               colors.button}
                    type="submit"
            >Clear</button>
        </form>
    )
}

function Input({o, onChange}) {
    const [inputValue, setInputValue] = useState('')
    if (o !== null) o.setSetInputValue(setInputValue)
    const inpRef = useRef(null)
    useEffect(function() {
        const t = inpRef.current
        t.style.height = 'auto'
        t.style.height = t.scrollHeight + 'px'
    }, [])
    return (
        <div className={styles.messengerInputContainer}>
            <textarea
                ref={inpRef}
                name="message"
                placeholder="Think and type"
                className={styles.messengerInput + ' ' + colors.input}
                value={inputValue}
                onChange={onChange}
            />
        </div>
    )
}
