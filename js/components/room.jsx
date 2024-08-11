import Moments from '../components/moments.jsx'
import InputAndButton from '../components/inputAndButton.jsx'
import styles from './room.module.css'

export default function Room({o}) {
    return (
        <main className={styles.main + ' ' + styles.bgPale}>
            <Moments o={o} />
            <InputAndButton
                o={o}
                className={styles.stickyBottom} />
        </main>
    )
}
