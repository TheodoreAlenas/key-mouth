import IoHome from '../mod/io/IoHome.js'
import UriHome from '../mod/io/UriHome.js'
import uriFirstArg from '../mod/io/uriFirstArg.js'
import Layout from '../components/layout.jsx'
import styles from '../components/styles.module.css'

export default function PageIndex({uriFirstArg}) {
    const io = new IoHome({uri: new UriHome(uriFirstArg.home)})
    return <Layout io={io} styles={styles}>
               <div className={styles.centeredMessage}>
                   Please select a chat room from the menu.
               </div>
           </Layout>
}

export async function getStaticProps() {
    return {props: {uriFirstArg}}
}
