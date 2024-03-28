import React from 'react'
import newsList from '../assets/data'
import ListItem from '../components/ListItem'

const NewsListPage = () => {
  return (
    <div className="news">
      <div className="news-header">
        <h2 className="news-title">News</h2>
        <p className="news-count">{newsList.length}</p>
      </div>
      <div className="news-list">
        {newsList.map((news, index) => (
            <ListItem key={index} news={news}/>
        ))}
      </div>
    </div>
    
  )
}

export default NewsListPage