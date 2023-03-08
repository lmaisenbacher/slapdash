import * as React from "react";
import { ComponentType, ComponentLabel } from "./component";
import MetadataProps from "./metadata";
import Form from 'react-bootstrap/Form'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import {Tooltip as BootstrapTooltip} from 'react-bootstrap';

interface EnumProps {
  value: any;
  name: string;
  enums: string[];
  type: ComponentType;
  readonly: boolean;
  fullName: string;
  doc?: string;
  metadata?: MetadataProps;
  update: (name: string, value: any) => void;
  gui_alert: (message: string) => void;
}
export default class ComponentEnum extends React.PureComponent<
  EnumProps,
  { value: string; edit: boolean }
> {
  constructor(props) {
    super(props);
    this.state = {
      value: this.props.value,
      edit: false,
    };
    this.onFocus = this.onFocus.bind(this);
    this.updateValue = this.updateValue.bind(this);
    this.onBlur = this.onBlur.bind(this);
  }

  onFocus() {
    // turn editing on
    // replace value with the local state value
    this.setState({ value: this.props.value, edit: true });
  }

  updateValue() {
    // if the component value has changed, update it
    if (this.state.value != this.props.value) {
      this.props.update(this.props.fullName, this.state.value);
    }
  }

  onBlur() {
    this.updateValue();
    // turn editing off
    this.setState({ edit: false });
  }

  render() {
    let props = {
      name: this.props.name,
      fullname: this.props.fullName,
      disabled: this.props.readonly != undefined,
      docString: this.props?.metadata?.doc ? this.props?.metadata.doc : (this.props?.doc ? this.props.doc : ''),
      onFocus: this.onFocus,
      onBlur: this.onBlur,
      onChange: (event) => this.setState({ value: event.target.value }),
      onKeyUp: (event) => {
        if (event.key === "Enter") {
          this.updateValue();
        }
      },
      value: this.state.edit ? this.state.value : this.props.value,
    };

    const tooltip = (props.docString) ? (<BootstrapTooltip className="tooltip">{props.docString}</BootstrapTooltip>) : null;

    // this injects arbitrary objects in props, without a way to check them. Is it bad?
    if (this.props.metadata !== undefined) {
      props = { ...props, ...this.props.metadata };
    }

    const enums = this.props.enums.map((name, index) => (
      <option key={index} value={name}> {name} </option>
    ));

    const { fullname, docString, ...validProps } = props

    return (
      <OverlayTrigger
        placement="top"
        overlay={tooltip}
      >
      {({ref, ...triggerHandler }) => (
        <div className="component enum" id={props.fullname}>
          <ComponentLabel ref={ref} overlayTrigger={triggerHandler} {...props}/>
          <Form.Select name={props.name} value={props.value} {...validProps}>
            {enums}
          </Form.Select>
        </div>
      )}
      </OverlayTrigger>
    );
  }
}
