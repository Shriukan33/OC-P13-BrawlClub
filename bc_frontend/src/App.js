import './App.css';
import Layout from './common/Layout';
import Home from './home/Home';
import Player from './player/Player';
import Club from './club/Club';
import Leaderboard from './leaderboard/Leaderboard_app';
import { Route, Routes } from 'react-router-dom';
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
    return (
        <>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<Home />} />
                    <Route path="player">
                        <Route index path=":tag" element={<Player />} />
                    </Route>
                    <Route path="club">
                        <Route index path=":tag" element={<Club />} />
                    </Route>
                    <Route path="leaderboard">
                        <Route index path=":entity" element={<Leaderboard />} />
                    </Route>
                </Route>
            </Routes>
        </>
    );
}

export default App;
