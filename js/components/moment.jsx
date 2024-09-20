
export default function Moment({moment, styles}) {
    try {
        const m = moment
        const namesAndCommas = m.names.reduce((a, x) => a + ', ' + x, '')
        const msgs = m.messages.map(
            (person, i) => PersonToLi({person, i, styles}))
        return (
            <section key={m.key} className={styles.moment} tabIndex='0'>
                <h2 className={styles.bubbleTop}>
                    {(m.time || '') + namesAndCommas}
                </h2>
                <ul className={styles.bubbleGroup + ' ' +
                               styles.bubbleGroupSpacing + ' ' +
                               styles.noBullets}>
                    {msgs}
                </ul>
            </section>
        )
    }
    catch (e) {
        console.error("error rendering moment:")
        console.error(moment)
        throw e
    }
}

function PersonToLi({person, i, styles}) {
    try {
        return <li id={person.id} key={i}>
                   <pre className={styles.bubble}>
                       {person.map(
                           (diff, i) => DiffToSpan({diff, i, styles}))}
                   </pre>
               </li>
    }
    catch (e) {
        console.error("error rendering person " + i + ':')
        console.error(person)
        throw e
    }
 }

function DiffToSpan({diff, i, styles}) {
    if (diff.type === "write") {
        return <span key={i}>{diff.body}</span>
    }
    if (diff.type === "delete") {
        return <del className={styles.delete}
                    key={i}>{diff.body}</del>
    }
    if (diff.type === "erase") {
        return <del className={styles.erase}
                    key={i}>{diff.body}</del>
    }
    if (diff.type === "event") {
        return <code className={styles.event}
                     key={i}>{diff.body}</code>
    }
    else return <code key={i}>ERROR</code>
}
