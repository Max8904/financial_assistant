import React from 'react'
import newsList from '../assets/data'
import ListItem from '../components/ListItem'

const NewsListPage = () => {
  return (
    <div>
        {newsList.map((news, index) => (
            <ListItem key={index} news={news}/>
        ))}
    </div>
  )
}

export default NewsListPage