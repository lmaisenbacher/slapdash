import * as React from "react";
import * as _ from "lodash/fp";
import Component, { ComponentType } from "./component";
import ComponentGroup from "./group";
import ComponentEnum from "./enum";
import Method from "./method";
import MetadataProps from "./metadata";
import Collapsible from "react-collapsible";
import Badge from 'react-bootstrap/Badge'

interface ArrayProps {
  name: string;
  parent?: string;
  param_value: any;
  param_props: any;
  update: (name: string, value: any) => void;
  metadata?: MetadataProps;
  api: string;
  collapsible?: boolean; // arrays are always collapsible
  collapsed?: boolean;
  instant_update?: boolean;
  readonly?: boolean;
  gui_alert: (message: string) => void;
}

const ComponentArray: React.FunctionComponent<ArrayProps> = ({
  name,
  parent,
  param_value,
  param_props,
  update,
  metadata,
  api,
  collapsible,
  collapsed,
  instant_update,
  readonly,
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

  // build up "params" object by iterating through components in the array
  const params = param_props.map((props, index) => {
    const value = param_value[index];
    if (
      props == ComponentType.Bool ||
      props == ComponentType.Int ||
      props == ComponentType.Float ||
      props == ComponentType.String
    ) {
      return (
        <Component
          key={index}
          value={value}
          type={props}
          readonly={readonly}
          // name={`${name}[${index}]`}
          name={`[${index}]`}
          fullName={`${parent}[${index}]`}
          update={update}
          metadata={_.omit(['doc', 'displayName'], metadata)}
          instant_update={instant_update}
          gui_alert={gui_alert}
        />
      );
    } else if (props == ComponentType.Enum) {
      // CM: workaround, because the full props are not passed in Arrays, only the types
      return (
        <Component
          key={index}
          value={value}
          type={ComponentType.String}
          readonly={true}
          name={`${name}[${index}]`}
          fullName={`${parent}[${index}]`}
          update={(name, value) => undefined}
          instant_update={instant_update}
          gui_alert={gui_alert}
        />
      );
    } else if (props.type == ComponentType.Method) {
      return (
        <Method
          key={index}
          {...props}
          fullName={`${parent}[${index}]`}
          api={api}
          gui_alert={gui_alert}
        />
      );
    } else if (Array.isArray(props)) {
      return (
        <ComponentArray
          key={index}
          name={`${name}[${index}]`}
          parent={`${parent}[${index}]`}
          param_value={value}
          param_props={props}
          update={update}
          metadata={metadata}
          api={api}
          collapsed={collapsed}
          instant_update={instant_update}
          readonly={readonly}
          gui_alert={gui_alert}
        />
      );
    } else if (props instanceof Object) {
      return (
        <ComponentGroup
          key={index}
          name={`${name}[${index}]`}
          parent={`${parent}[${index}]`}
          param_value={value}
          param_props={props}
          update={update}
          metadata={metadata}
          api={api}
          collapsed={collapsed}
          instant_update={instant_update}
          gui_alert={gui_alert}
        />
      );
    }
  });
  const elementProps = { className: "array", id: parent };

  function determineOpen() {
    const isOpen = (collapsed === undefined ? !collapsedState : !collapsed);
    return isOpen;
  }

  const tooltipStatic = (metadata?.doc !== undefined) ? <div className={"array-tooltip"}><Badge pill className="tooltip-trigger" bg="secondary">?</Badge>{metadata?.doc}</div> : null;

  const displayName = (metadata?.displayName !== undefined ) ? ((name.indexOf('[') >= 0) ? metadata.displayName + ' ' + name.slice(name.indexOf('[')) : metadata.displayName) : name;

  // wrap "params" in a collapsible div and add a tooltip if applicable
  return (
    <Collapsible
      containerElementProps={elementProps}
      contentInnerClassName={"array__contentInner"}
      trigger={displayName}
      triggerDisabled={disableCollapse}
      open={disableCollapse ? true : determineOpen()}
      transitionTime={200}
      onClosing={() => {setCollapsedState(true); saveOpen(name, true);}}
      onOpening={() => {setCollapsedState(false); saveOpen(name, false);}}
    >
      {tooltipStatic}
      <div className={"component-array"}>{params}</div>
    </Collapsible>
  );
};

ComponentArray.defaultProps = {
  parent: "",
};

export default React.memo(ComponentArray);
