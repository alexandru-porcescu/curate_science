import React from 'react';
import PropTypes from 'prop-types';

// Routing & routes
import { BrowserRouter as Router, Redirect, Route, Switch } from "react-router-dom";

import EmbeddedViewer from './components/EmbeddedViewer.jsx';
import ScrollToTop from './components/ScrollToTop.jsx';
import TopBar, { TOPBAR_HEIGHT } from './components/TopBar.jsx';
import Footer from './components/Footer.jsx';
import { ViewURL } from './components/EmbeddedViewer.jsx';

import Splash from './pages/Splash.jsx';
import Help from './pages/Help.jsx';
import Home from './pages/Home.jsx';
import Privacy from './pages/Privacy.jsx';
import Recent from './pages/Recent.jsx';
import Replications from './pages/Replications.jsx';
import ArticlePage from './pages/ArticlePage.jsx';
import AuthorPage from './pages/AuthorPage.jsx';
import AuthorPageCreator from './pages/AuthorPageCreator.jsx';
import AdminManage from './pages/AdminManage.jsx';
import AdminInvite from './pages/AdminInvite.jsx';
import SearchResults from './pages/SearchResults.jsx';

// UI components
import { fade } from '@material-ui/core/styles/colorManipulator';
import { withStyles } from '@material-ui/core/styles';
import {AppBar, Toolbar, Typography, IconButton, Button, Grid, Menu, MenuItem} from '@material-ui/core';
import CssBaseline from '@material-ui/core/CssBaseline';

// Theme
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
// import 'typeface-roboto'

import C from './constants/constants';

import css from './App.css';

const theme = createMuiTheme({
  palette: {
    primary: { main: '#793DF7' },
    secondary: { main: '#8F0DCC' },
    bg: '#FFF'
  },
  typography: {
    useNextVariants: true,
    fontSize: 12,
    h2: {
        marginTop: 10,
        marginBottom: 10
    },
    h3: {
        marginTop: 20,
    },
    h4: {
        textTransform: 'uppercase',
        fontSize: 18,
        color: 'gray'
    }
  },
  overrides: {
    MuiButton: {
        containedPrimary: {
            background: 'linear-gradient(45deg, #4F0FF8 30%, #793DF7 90%)',
        },
        sizeLarge: {
           padding: 20
        }
    },
    MuiTooltip: {
        tooltip: {
            fontSize: 13
        }
    }
  }
});

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {

        };
    }

    render() {
        const { classes, user_session } = this.props;
        return (
        	<Router basename="/app">
                <ScrollToTop/>
                <div style={{backgroundColor: theme.palette.bg}}>
                    <MuiThemeProvider theme={theme}>
                        <Switch>
                            // Author embed page
                            <Route
                                path="/author-embed/:slug(.+)"
                                component={() => <AuthorPage user_session={{}} embedded={true}/>}
                            />

                            // Rest of the app
                            <Route>
                                <TopBar user_session={user_session} />
                                <div style={{display: 'flex'}}>
                                <ViewURL.Provider>
                                <div className="AppContent" style={{ marginTop: TOPBAR_HEIGHT }}>
                                    <Switch>
                                        <Route
                                            exact path="/"
                                            component={() =>  {
                                                if (user_session.authenticated) {
                                                    return <Redirect to="/recent"/>
                                                }
                                                return <Redirect to="/home"/>
                                            }}
                                        />
                                        <Route
                                            exact path="/home"
                                            component={() => <Home user_session={user_session} />}
                                        />
                                        <Route
                                            exact path="/recent"
                                            component={() => <Recent user_session={user_session} />}
                                        />
                                        <Route exact path="/replications" component={Replications} />
                                        <Route path="/help" component={Help} />
                                        <Route path="/privacy" component={Privacy} />
                                        <Route path="/author/:slug(.+)" component={() => <AuthorPage user_session={user_session} />} />
                                        <Route path="/article/:id" component={() => <ArticlePage user_session={user_session} />} />
                                        <Route path="/create_author" component={() => <AuthorPageCreator user_session={user_session} />} />
                                        <Route path="/search" component={() => <SearchResults user_session={user_session} />} />
                                        <Route path="/admin/manage" component={AdminManage} />
                                        <Route path="/admin/invite" component={AdminInvite} />
                                    </Switch>
                                    </div>
                                    <EmbeddedViewer/>
                                    </ViewURL.Provider>
                                </div>
                                <Route
                                    exact path="/home"
                                    component={() => <Footer />}
                                />
                            </Route>
                        </Switch>
                    </MuiThemeProvider>
                </div>
            </Router>
        );
    }
}

App.defaultProps = {
}

export default App;
