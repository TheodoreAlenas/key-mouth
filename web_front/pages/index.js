import sayHi from '../../a_feature/say_hi.mjs'

export default function Home() {
    return (
        <>
            <h1>{sayHi()}</h1>
            <table>
                <thead>
                    <tr><td>Name</td><td>Message</td></tr>
                </thead>
                <tbody>
                    <tr><td>Sotiris</td><td>Hi Mark</td></tr>
                    <tr><td>Sotiris</td><td>Are you there?</td></tr>
                </tbody>
            </table>
            <section>
                <ul>
                    <li>Hi Mark</li>
                    <li>Are you there?</li>
                </ul>
            </section>
            <input type="text" />
            <button>Send and clear</button>
        </>)
}
