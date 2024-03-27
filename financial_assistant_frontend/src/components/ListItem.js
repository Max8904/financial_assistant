import React from 'react'
import {Link} from 'react-router-dom'

const ListItem = ({news}) => {
  return (
    <Link to={`news/${news.id}`}>
      <h3>{news.body}</h3>
    </Link>
  )
}

export default ListItem