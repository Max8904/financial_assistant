import React from 'react'

const ListItem = ({news}) => {
  return (
    <div>
        <h3>{news.body}</h3>
    </div>
  )
}

export default ListItem