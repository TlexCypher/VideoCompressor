import Board from "./components/Board.tsx";
import Layout from "./components/Layout.tsx";
import axios from 'axios'

const App = () => {
    axios.defaults.baseURL = "http://127.0.0.1:5000"
    return (
        <Layout>
            <Board/>
        </Layout>
    )
}

export default App;