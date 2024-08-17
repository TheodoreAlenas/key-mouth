import Moments from '../components/moments.jsx'
import InputAndButton from '../components/inputAndButton.jsx'
import shapes from './shapes.module.css'
import colors from './colors.module.css'

export default function Room({o}) {
    return (
        <main className={shapes.bg + ' ' + colors.bg}>
            <Moments o={o} />
            <InputAndButton
                o={o}
                className={shapes.stickyBottom} />
        </main>
    )
}
