import React from 'react'
import {Link} from 'react-router-dom'

const ListItem = ({news}) => {
  return (
    <Link to={`news/${news.id}`}>
      <div className="news-list-item">
        <h3>{news.body}</h3>
      </div>
    </Link>
  )
}

export default ListItem