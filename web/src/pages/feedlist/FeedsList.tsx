import React from "react";
import FeedCard from "./FeedCard";

export interface IFeeds {
    "feedCreator": string,
    "name": string
}

class Feeds extends React.Component {
    data: IFeeds

    constructor(props: Readonly<IFeeds>) {
        super(props)
        this.data = {
            "feedCreator": "feedCreator",
            "name": 'name'
        }
    }

  render() {
    return (
      <div className="feeds">
         <FeedCard feedCreator={this.data.feedCreator} feedName={this.data.name} />
      </div>
    );
  }
}

export default Feeds;
