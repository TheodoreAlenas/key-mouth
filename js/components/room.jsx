import Moments from '../components/moments.jsx'
import InputAndButton from '../components/inputAndButton.jsx'
import shapes from './shapes.module.css'

export default function Room({o}) {
    return (
        <main className={shapes.thinCentered + ' ' + shapes.bgPale}>
            <Moments o={o} />
            <InputAndButton
                o={o}
                className={shapes.stickyBottom} />
        </main>
    )
}
