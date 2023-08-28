interface Props {
  name: string;
  description: string;
}

const SubedChannelsCard = (props: Props) => {
  return (
    <div className="col-lg-4 box-element">
      <div className="row">
        <div className="col-lg-12">
          <h3>{props.name}</h3>
        </div>
      </div>
      <div className="row">
        <div className="col-lg-12">
          <h5>{props.description}</h5>
        </div>
      </div>
    </div>
  );
};

export default SubedChannelsCard;
