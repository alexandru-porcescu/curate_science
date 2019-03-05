import React from 'react';

import {IconButton} from '@material-ui/core';
import C from '../constants/constants';

class AuthorLinks extends React.Component {
	constructor(props) {
        super(props);
        this.state = {
        };

        this.render_link = this.render_link.bind(this)
    }

	render_link(url, link_type) {
		let st = {
			marginLeft: 3,
			opacity: 0.5
		}
		if (link_type == 'email') url = 'mailto:' + url
		return <IconButton href={url} key={link_type} style={st} target="_blank"><img width={25} src={`/sitestatic/icons/${link_type}.svg`} /></IconButton>
	}

	render() {
		let {links} = this.props
		let links_rendered = []
		if (links == null) links = {}
		C.AUTHOR_LINKS.forEach((al) => {
			if (links[al.id] != null) {
				links_rendered.push(this.render_link(links[al.id], al.id))
			}
		})
		return (
			<div className="authorLinks center-block" style={{textAlign: 'center'}}>
			 { links_rendered }
			</div>
		)
	}
}

AuthorLinks.defaultProps = {
	links: {}
};

export default AuthorLinks;