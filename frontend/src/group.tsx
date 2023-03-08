import * as React from "react";
import Component, { ComponentType } from "./component";
import ComponentArray from "./array";
import ComponentEnum from "./enum";
import Method from "./method";
import MetadataProps from "./metadata";
import Collapsible from "react-collapsible";
import Badge from 'react-bootstrap/Badge'


type GroupProps = {
  name: string;
  parent?: string;
  param_value: any;
  param_props: any;
  api: string;
  doc?: string;
  metadata?: MetadataProps;
  collapsible?: boolean; // the root group is not collapsible
  collapsed?: boolean; // whether a collapse is requested from the parent (PROP, not STATE)
  instant_update?: boolean;
  update: (name: string, value: any) => void;
  gui_alert: (message: string) => void;
};

const ComponentGroup: React.FunctionComponent<GroupProps> = ({
  name,
  parent,
  param_value,
  param_props,
  update,
  api,
  doc,
  metadata, // is implicitly passed through {...props}
  collapsible,
  collapsed,
  instant_update,
  gui_alert
}) => {
  const [collapsedState, setCollapsedState] = React.useState(localStorage.getItem(name + '_collapsed') == 'true');
  const [disableCollapse, setDisableCollapse] = React.useState(collapsible === undefined ? false : !collapsible);

  // React.useEffect(() => {
  //   localStorage.setItem(name + '_collapsed', JSON.stringify(collapsed));
  // }, [collapsedState]);

  function saveOpen(name, collapsed) {
    localStorage.setItem(name + '_collapsed', JSON.stringify(collapsed));
  };

  // build up "params" object by iterating through components in the group
  const params = Object.keys(param_props).map((name, index) => {
    const value = param_value[name];
    const props = param_props[name];

    if (
      props.type == ComponentType.Bool ||
      props.type == ComponentType.Int ||
      props.type == ComponentType.Float ||
      props.type == ComponentType.String ||
      props.type == ComponentType.Array
    ) {
      return (
        <Component
          key={index}
          value={value}
          {...props}
          fullName={parent == "" ? name : parent + "." + name}
          update={update}
          instant_update={instant_update}
          gui_alert={gui_alert}
        />
      );
    } else if (props.type == ComponentType.Enum) {
      return (
        <ComponentEnum
          key={index}
          value={value}
          {...props}
          fullName={parent == "" ? name : parent + "." + name}
          api={api}
          update={update}
          gui_alert={gui_alert}
        />
      );
    } else if (props.type == ComponentType.Method) {
      return (
        <Method
          key={index}
          {...props}
          fullName={parent == "" ? name : parent + "." + name}
          api={api}
          collapsed={collapsed}
          gui_alert={gui_alert}
        />
      );
    } else if (Array.isArray(props.type)) {
      return (
        <ComponentArray
          key={index}
          name={name}
          parent={parent == "" ? name : parent + "." + name}
          param_value={value}
          param_props={props.type}
          update={update}
          {...props}
          api={api}
          collapsed={collapsed}
          instant_update={instant_update}
          gui_alert={gui_alert}
        />
      );
    } else if (props.type instanceof Object) {
      return (
        <ComponentGroup
          key={index}
          name={name}
          parent={parent == "" ? name : parent + "." + name}
          param_value={value}
          param_props={props.type}
          update={update}
          {...props}
          api={api}
          collapsed={collapsed}
          instant_update={instant_update}
          gui_alert={gui_alert}
        />
      );
    } else {
      return null;
    }
  });
  const elementProps = { className: "group", id: parent };

  function determineOpen() {
    const isOpen = (collapsed === undefined ? !collapsedState : !collapsed);
    return isOpen;
  }

  const tooltipStatic = (doc !== undefined) ? <div className={"group-tooltip"}><Badge pill className="tooltip-trigger" bg="secondary">?</Badge>{doc}</div> : null;

  // wrap "params" in a collapsible div and add a tooltip if applicable
  return (
    <Collapsible
      containerElementProps={elementProps}
      contentInnerClassName={"group__contentInner"}
      trigger={name}
      triggerDisabled={disableCollapse}
      open={disableCollapse ? true : determineOpen()}
      transitionTime={200}
      onClosing={() => {setCollapsedState(true); saveOpen(name, true);}}
      onOpening={() => {setCollapsedState(false); saveOpen(name, false);}}
    >
      {tooltipStatic}
      <div className="component-group">{params}</div>
    </Collapsible>
  );
};

ComponentGroup.defaultProps = {
  parent: "",
};

export default React.memo(ComponentGroup);
