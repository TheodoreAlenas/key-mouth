import Moments from '../components/moments.jsx'
import InputAndButton from '../components/inputAndButton.jsx'

export default function Room({o, styles}) {
    return (
        <>
            <Moments o={o} styles={styles} />
            <InputAndButton o={o} styles={styles} />
        </>
    )
}
