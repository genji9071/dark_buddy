import React, { Component } from "react";
import Card_1 from "./Card_1";
import Card_2 from "./Card_2";
import Card_3 from "./Card_3";

export interface ICard {
    "heading": string,
    "messageLink": string,
    "image": string
}

class CardsList extends React.Component<{cards:[ICard]}> {

    cards: [ICard]

    constructor(props) {
        super(props)
        this.cards = props.cards
    }

    render() {
        return (
            <div>
                {
                    this.cards.map(card => {
                        return <Card_1 cardData={card} />
                    })
                }
            </div>

        );
    }
}

export default CardsList;
