import React from 'react';
import PropTypes from 'prop-types';

// Routing & routes
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";

import TopBar from './components/TopBar.jsx';

import Splash from './pages/Splash.jsx';
import About from './pages/About.jsx';
import FAQ from './pages/FAQ.jsx';
import Privacy from './pages/Privacy.jsx';
import Recent from './pages/Recent.jsx';
import Replications from './pages/Replications.jsx';
import AuthorPage from './pages/AuthorPage.jsx';
import AuthorPageCreator from './pages/AuthorPageCreator.jsx';
import AdminManage from './pages/AdminManage.jsx';
import AdminInvite from './pages/AdminInvite.jsx';
import Footer from './components/Footer.jsx';

// UI components
import { fade } from '@material-ui/core/styles/colorManipulator';
import { withStyles } from '@material-ui/core/styles';
import {AppBar, Toolbar, Typography, IconButton, Button, Grid, Menu, MenuItem} from '@material-ui/core';
import CssBaseline from '@material-ui/core/CssBaseline';

// Theme
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
// import 'typeface-roboto'

import C from './constants/constants';

// CS components
import ArticleLI from './components/ArticleLI.jsx';

import css from './App.css';

const theme = createMuiTheme({
  palette: {
    primary: { main: '#793DF7' },
    secondary: { main: '#8F0DCC' },
    bg: '#EEE'
  },
  typography: {
    useNextVariants: true,
    fontSize: 12,
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
        const { anchorEl } = this.state;
        const open = Boolean(anchorEl);
        return (
        	<Router forceRefresh={true} basename="/app">
                <div style={{backgroundColor: theme.palette.bg}}>
                    <MuiThemeProvider theme={theme}>
                        <TopBar user_session={user_session} />
                        <div className="AppContent">
                            <Switch>
                                <Route exact path="/" component={Recent} />
                                <Route exact path="/recent" component={Recent} />
                                <Route exact path="/replications" component={Replications} />
                                <Route path="/about" component={About} />
                                <Route path="/faq" component={FAQ} />
                                <Route path="/privacy" component={Privacy} />
                                <Route path="/author/:slug(.+)" component={() => <AuthorPage user_session={user_session} />} />
                                <Route path="/create_author" component={() => <AuthorPageCreator user_session={user_session} />} />
                                <Route path="/admin/manage" component={AdminManage} />
                                <Route path="/admin/invite" component={AdminInvite} />
                            </Switch>
                        </div>
                        <Footer />
                    </MuiThemeProvider>
                </div>
            </Router>
        );
    }
}

App.defaultProps = {
}

export default App;
