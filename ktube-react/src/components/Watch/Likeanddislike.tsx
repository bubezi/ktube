interface Props {
    likes: number,
    dislikes: number,
}

export default function Likeanddislike (props: Props) {
    const Likes = ()=>{
        if (props.likes === 1){return (<h6><strong id="likes-count">{props.likes} like</strong></h6>);
        }else{return (<h6><strong id="likes-count">{props.likes} likes</strong></h6>);}
    }
    const DisLikes = ()=>{
        if (props.dislikes === 1){return (<h6><strong id="dislikes-count">{props.dislikes} dislike</strong></h6>);
        }else{return (<h6><strong id="dislikes-count">{props.dislikes} dislikes</strong></h6>);}
    }
    return (
    <>
    <div className="row">
        <Likes/>
        <DisLikes/>
    </div>
    <div className="row">
        
    </div>
    </>
    );
}