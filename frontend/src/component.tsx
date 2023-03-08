import * as React from "react";
import MetadataProps from "./metadata";
import RangeSlider from 'react-bootstrap-range-slider';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import {Tooltip as BootstrapTooltip} from 'react-bootstrap';
import Badge from 'react-bootstrap/Badge'
import NumericInput from "./NumericInput";
import {fnCalcPrecision, fnCalcStep, precisionFormatter, fnKeyDown, fnClampNumericTyping, fnHandleNumChange} from './NumericHelpers';
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Label, ResponsiveContainer} from "recharts";

function sanitizeIntegerStep(step: number) {
  var newStep: number = step;
  if (step < 1) {
    newStep = 1;
  } else if (step > 1) {
    newStep = Math.round(step);
  }
  return newStep;
}

export enum ComponentType {
  Bool = "bool",
  Int = "int",
  Float = "float",
  String = "str",
  Method = "method",
  Enum = "enum",
  Array = "array"
}

interface ComponentProps {
  value: any;
  name: string;
  type: ComponentType;
  readonly: boolean;
  fullName: string;
  update: (name: string, value: any) => void;
  doc?: string;
  metadata?: MetadataProps;
  instant_update?: boolean;
  gui_alert: (message: string) => void;
}
export default class Component extends React.PureComponent<
  ComponentProps,
  { value: string; edit: boolean } // state values of the component
> {
  constructor(props) {
    super(props);
    this.state = {
      value: this.props.value, // connects App props value with Component state
      edit: false,
    };
    this.onFocus = this.onFocus.bind(this);
    this.updateValue = this.updateValue.bind(this);
    this.onBlur = this.onBlur.bind(this);
    this.quickSetState = this.quickSetState.bind(this);
    this.ensureEdit = this.ensureEdit.bind(this);
    this.gui_alert = this.gui_alert.bind(this);
  }

  onFocus() {
    // turn editing on
    // replace value with the local state value
    if (!this.state.edit) {
      this.setState({ value: this.props.value, edit: true });
    }
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

  ensureEdit() {
    // ensure we are in editing mode, without replacing value
    this.setState({ edit: true });
  }

  quickSetState(event) {
    // take up the state while continuing in editing state;
    // intended for one-time manual changes
    this.setState({ value: event.target.value });
    this.updateValue();
  }

  gui_alert(message) {
    this.props.gui_alert(message);
  }

  render() {
    let props = {
      name: this.props.name,
      fullname: this.props.fullName,
      readOnly: this.props.readonly != undefined,
      docString: this.props?.metadata?.doc ? this.props?.metadata.doc : (this.props?.doc ? this.props.doc : ''),
      onFocus: this.onFocus,
      onBlur: this.onBlur,
      onChange: this.props.instant_update ?
        (event) => {this.props.update(this.props.fullName, event.target.value); this.setState({ value: event.target.value })} :
        (event) => {this.setState({ value: event.target.value })}, // onChange for the Component, passed via {...props}
      onKeyUp: (event) => {
        if (event.key === "Enter") {
          this.onBlur();
        }
      },
      value: this.state.edit ? this.state.value : this.props.value, // Component.props.value passed to Subcomponent.props.value
    };

    const tooltip = (props.docString) ? (<BootstrapTooltip className="tooltip">{props.docString}</BootstrapTooltip>) : null;

    // this injects arbitrary metadata key-value pairs into props, without a way to check them, watch out!
    if (this.props.metadata !== undefined) {
      props = { ...props, ...this.props.metadata };
    }

    const iuObj = {instantUpdate: this.props.instant_update};
    let instantProps = {...props, ...iuObj};

    var {onKeyUp, ...stringProps} = props;
    const isTextArea = (this.props.metadata?.renderAs == 'textarea');
    if (!isTextArea) {
      stringProps = props;
    }

    if (this.props.type === ComponentType.Int) {
      if (this.props.metadata !== undefined && (this.props.metadata.isSlider || this.props.metadata.renderAs == 'slider')) {
        return (
          <OverlayTrigger
            placement="top"
            overlay={tooltip}
          >
            {({ref, ...triggerHandler }) => (
            <ComponentSlider // integer slider component
              {...props}
              type={this.props.type}
              stepSize={(this.props.metadata?.step !== undefined) ? sanitizeIntegerStep(this.props.metadata.step) : 1}
              quickSetState={(event) => {this.quickSetState(event)}}
              instantUpdate={this.props.instant_update}
              ref={ref}
              overlayTrigger={triggerHandler}
              ensureEdit={() => this.ensureEdit()}
              gui_alert={(message) => this.gui_alert(message)}
            />
          )}
          </OverlayTrigger>
        );
      } else {
        return (
          <OverlayTrigger
            placement="top"
            overlay={tooltip}
          >
            {({ref, ...triggerHandler }) => (
            <ComponentNumber // integer numeric component
              {...props}
              type={this.props.type}
              instantUpdate={this.props.instant_update}
              ref={ref}
              overlayTrigger={triggerHandler}
              ensureEdit={() => this.ensureEdit()}
              gui_alert={(message) => this.gui_alert(message)}
            />
          )}
          </OverlayTrigger>
        )
      }

    } else if (this.props.type === ComponentType.Float) {
      if (this.props.metadata !== undefined && (this.props.metadata.isSlider || this.props.metadata.renderAs == 'slider')) {
        return (
          <OverlayTrigger
            placement="top"
            overlay={tooltip}
          >
            {({ref, ...triggerHandler }) => (
            <ComponentSlider // float slider component
              {...props}
              type={this.props.type}
              stepSize={(this.props.metadata.step !== undefined) ? this.props.metadata.step : 1e-9}
              quickSetState={(event) => {this.quickSetState(event)}}
              instantUpdate={this.props.instant_update}
              ref={ref}
              overlayTrigger={triggerHandler}
              ensureEdit={() => this.ensureEdit()}
              gui_alert={(message) => this.gui_alert(message)}
            />
            )}
          </OverlayTrigger>
        );
      } else {
        return (
          <OverlayTrigger
            placement="top"
            overlay={tooltip}
          >
            {({ref, ...triggerHandler }) => (
            <ComponentNumber // float numeric component
              {...props}
              type={this.props.type}
              instantUpdate={this.props.instant_update}
              ref={ref}
              overlayTrigger={triggerHandler}
              ensureEdit={() => this.ensureEdit()}
              gui_alert={(message) => this.gui_alert(message)}
            />
          )}
          </OverlayTrigger>
        )
      }
    } else if (this.props.type === ComponentType.String) {
      if (this.props.metadata !== undefined && (this.props.metadata.isImage || this.props.metadata.renderAs == 'image')) {
        return (
          <OverlayTrigger
            placement="top"
            overlay={tooltip}
          >
          {({ref, ...triggerHandler }) => (
            <ComponentBase64Image // string base64 image component
              {...props}
              ref={ref}
              overlayTrigger={triggerHandler}
            />
          )}
        </OverlayTrigger>
        )
      } else if (this.props.metadata !== undefined && (this.props.metadata.isDataStream || this.props.metadata.renderAs == 'graph')) {
        return (
          <OverlayTrigger
            placement="top"
            overlay={tooltip}
          >
          {({ref, ...triggerHandler }) => (
            <ComponentLineSeries // string graph component
              {...props}
              ref={ref}
              overlayTrigger={triggerHandler}
            />
          )}
          </OverlayTrigger>
        )
      } else {
        return (
          <OverlayTrigger
            placement="top"
            overlay={tooltip}
          >
            {({ref, ...triggerHandler }) => (
            <ComponentText // text component
              {...stringProps}
              instantUpdate={this.props.instant_update}
              ref={ref}
              overlayTrigger={triggerHandler}
              textArea={isTextArea}
            />
          )}
          </OverlayTrigger>
        )
      }
    } else if (this.props.type === ComponentType.Array) {
      return (
        <OverlayTrigger
          placement="top"
          overlay={tooltip}
        >
        {({ref, ...triggerHandler }) => (
          <ComponentLineSeries // array graph component, but I don't think we ever get here
            {...props}
            ref={ref}
            overlayTrigger={triggerHandler}
          />
        )}
        </OverlayTrigger>
      )
    } else if (this.props.type === ComponentType.Bool) {
      return (
        <OverlayTrigger
          placement="top"
          overlay={tooltip}
        >
          {({ref, ...triggerHandler }) => (
          <ComponentButton // boolean button component
            {...props}
            onToggle={() =>
              this.props.update(this.props.fullName, !this.props.value)
            }
            ref={ref}
            overlayTrigger={triggerHandler}
          />
        )}
        </OverlayTrigger>
      );
    } else {
      return (
        <OverlayTrigger
          placement="top"
          overlay={tooltip}
        >
          {({ref, ...triggerHandler }) => (
          <ComponentText // default catch-all text component
            {...stringProps}
            instantUpdate={this.props.instant_update}
            ref={ref}
            overlayTrigger={triggerHandler}
            textArea={isTextArea}
          />
        )}
        </OverlayTrigger>
      )
    }
  }
}

function unitsSpan(units: string, props: any) {
  var name = 'units';
  if (props.disabled | props.readOnly) {
    name += ' disabled';
  }
  if (props.instantUpdate) {
    name += ' instant';
  }
  if (units !== undefined) {
    return <span className={name}>{units}</span>;
  }
}

function componentClass(props) {
  if ((props.readOnly) | (props.disabled)) {
    return "component"
  } else {
    if (props.instantUpdate == true) {
      return "component instant"
    } else {
      return "component"
    }
  }
}

export const ComponentLabel = React.memo(React.forwardRef(
  (props: {
    name: string;
    displayName?: string;
    overlayTrigger: any;
    docString: string;
  }, ref: any) => {
    let name = (props.displayName !== undefined) ? props.displayName : props.name;

    if (props.docString) {
      return (
          <h4 className="component-label">
          <p>{name}</p>
          <Badge pill className="tooltip-trigger" bg="light" text="dark" ref={ref} {...props.overlayTrigger}>?</Badge>
          </h4>
      )
    } else {
      return (
          <h4 className="component-label">
          <p>{name}</p>
          </h4>
      )
    }
  }
))

const ComponentNumberRef = React.forwardRef(
  (props: {
    name: string;
    value: number;
    type: ComponentType;
    fullname: string;
    instantUpdate?: boolean;
    readOnly: boolean;
    overlayTrigger: any;
    docString: string;
    units?: string;
    min?: number;
    max?: number;
    step?: number;
    onChange: (event) => void;
    onFocus: () => void;
    onBlur: () => void;
    ensureEdit: () => void;
    gui_alert: (message: string) => void;
  }, ref: any) => {

    var classname = componentClass(props) + " numeric";
    if ((typeof document != 'undefined') && 'ontouchstart' in document) {
      classname += " mobile";
    }

    let units = (props.units !== undefined) ? unitsSpan(props.units, {...props}) : null;

    return (
      <div className={classname} id={props.fullname}>
        <ComponentLabel ref={ref} {...props}/>
        <NumericInput
          value={props.value}
          className={"form-control"}
          onChange={(valueAsNumber: number, valueAsString: string, input) => {
            props.ensureEdit(); fnHandleNumChange(props)(valueAsNumber, valueAsString, input)
          }}
          onMouseDown={event => {return props.onFocus();}}
          onBlur={event => {props.onBlur();}}
          onKeyDown={fnKeyDown(props, fnHandleNumChange(props))}
          format={(n: number, stepSize: number) => precisionFormatter(n, stepSize)}
          disabled={props.readOnly}
          step={fnCalcStep(props)}
          min={props.min}
          max={props.max}
          // parse={fnParse}
          precision={fnCalcPrecision(props)} // must be integer >= 0
          style = {false}
          onNumericKeyDown = {fnClampNumericTyping(props)}
        />
        {units}
      </div>
    );
  }
);
const ComponentNumber = React.memo(ComponentNumberRef);

const ComponentTextRef = React.forwardRef(
  (props: {
    name: string;
    value: string;
    fullname: string;
    instantUpdate?: boolean;
    readOnly: boolean;
    overlayTrigger: any;
    docString: string;
    units?: string;
    textArea?: boolean | undefined;
    }, ref: any) => {
    const { instantUpdate, fullname, overlayTrigger, docString, name, textArea, renderAs, ...validProps } = props

    let units = (props.units !== undefined) ? unitsSpan(props.units, {...props}) : null;

    let content = (
      <input
        type="text"
        className="form-control"
        disabled={props.readOnly}
        name={props.name}
        {...validProps}
      ></input>
    );
    let addon = '';

    if (props.textArea) {
      addon = ' textarea';
      // const {renderAs, ...textAreaValidProps} = validProps;
      content = (
        <textarea
          className="form-control"
          disabled={props.readOnly}
          name={props.name}
          {...validProps}
        ></textarea>
      );
    }

    return (
      <div className={componentClass(props) + " string" + addon} id={props.fullname}>
        <ComponentLabel ref={ref} {...props}/>
        {content}
        {units}
      </div>
    );
  }
);
const ComponentText = React.memo(ComponentTextRef);

const ComponentButtonRef = React.forwardRef(
  (props: {
    name: string;
    fullname: string;
    value: boolean;
    readOnly: boolean;
    overlayTrigger: any;
    docString: string;
    onToggle: () => void;
    mapping?: Array<string>;
  }, ref: any) => {
    let name: string = "";
    if (props.mapping !== undefined) {
      name = props.value ? props.mapping[0] : props.mapping[1];
    } else {
      name = props.name;
    }
    if (props.docString) {
      return (
        <div className={"component boolean"} id={props.fullname} ref={ref} {...props.overlayTrigger}>
          <Button
            type={"button"}
            variant={props.value ? "success" : "secondary"}
            onMouseUp={props.onToggle}
            disabled={props.readOnly}
          >
            <p>{name}</p>
            <Badge pill className="tooltip-trigger" bg="light" text="dark">?</Badge>
          </Button>
        </div>
      );
    } else {
      return (
        <div className={"component boolean"} id={props.fullname}>
          <Button
            type={"button"}
            variant={props.value ? "success" : "secondary"}
            onMouseUp={props.onToggle}
            disabled={props.readOnly}
          >
            <p>{name}</p>
          </Button>
        </div>
      );
    }
  }
);
const ComponentButton = React.memo(ComponentButtonRef);


const ComponentBase64ImageRef = React.forwardRef(
  (props: {
    name: string;
    fullname: string;
    value: string;
    overlayTrigger: any;
    docString: string;
  }, ref: any) => {
    return (
      <div className="component image" id={props.fullname}>
        <ComponentLabel ref={ref} {...props}/>
        <div className="image-container">
          <p></p>
          <img src={`data:image/png;base64,${props.value}`} alt={props.name} />
          <p></p>
        </div>
      </div>
    );
  }
);
const ComponentBase64Image = React.memo(ComponentBase64ImageRef);


const ComponentSliderRef = React.forwardRef(
  (props: {
    name: string;
    fullname: string;
    type: ComponentType;
    value: number;
    instantUpdate?: boolean;
    readOnly: boolean;
    overlayTrigger: any;
    docString: string;
    units?: string;
    min?: number;
    max?: number;
    step?: number; // from metadata
    stepSize: number; // from number type (int or float)
    onChange: (event) => void;
    onFocus: () => void;
    onBlur: () => void;
    quickSetState: (event) => void;
    ensureEdit: () => void;
    gui_alert: (message: string) => void;
  }, ref: any) => {

    function handleOnChange(event, newNumber?: number) {
      props.onChange(event);
    }

    function handleMouseUp(event) {
      // register the change but stay in editing mode
      props.quickSetState(event);
    }

    var classname = componentClass(props) + " numeric";
    if ((typeof document != 'undefined') && 'ontouchstart' in document) {
      classname += " mobile";
    }

    let units = (props.units !== undefined) ? unitsSpan(props.units, {...props}) : null;

    return (
      <div className={componentClass(props) + " slider"} id={props.fullname}>
        <ComponentLabel ref={ref} {...props}/>
          <div className="component-slider">

          <Form className="slider-form">
            <Form.Group>
                <div>
                  <RangeSlider
                  disabled={props.readOnly}
                  value={props.value}
                  onMouseDown={(event) => props.onFocus()}
                  onClick={(event) => handleMouseUp(event)}
                  onChange={(event, newNumber) => handleOnChange(event, newNumber)}
                  onBlur={(event) => props.onBlur()}
                  onTouchStart={(event) => props.onFocus()}
                  onTouchEnd={(event) => props.onBlur()}
                  min={props.min}
                  max={props.max}
                  step={props.stepSize}
                  tooltip={'off'}
                />
              </div>


              <div className={classname + ' slider-input-container'}>
                <NumericInput
                  value={props.value}
                  className={"form-control"}
                  onChange={(valueAsNumber: number, valueAsString: string, input) => {
                    props.ensureEdit(); fnHandleNumChange(props)(valueAsNumber, valueAsString, input)
                  }}
                  onMouseDown={event => {return props.onFocus();}}
                  onBlur={event => {props.onBlur();}}
                  onKeyDown={fnKeyDown(props, fnHandleNumChange(props))}
                  format={(n: number, stepSize: number) => precisionFormatter(n, stepSize)}
                  disabled={props.readOnly}
                  step={fnCalcStep(props)}
                  min={() => {return props.min}}
                  max={() => {return props.max}}
                  precision={fnCalcPrecision(props)} // must be integer >= 0
                  style = {false}
                  onNumericKeyDown = {fnClampNumericTyping(props)}
                  />
                {units}
              </div>
            </Form.Group>
          </Form>

          </div>
      </div>
    );
  }
);
const ComponentSlider = React.memo(ComponentSliderRef);

const ComponentLineSeriesRef = React.forwardRef(
  (props: {
    name: string;
    fullname: string;
    value: string;
    overlayTrigger: any;
    docString: string;
    units?: string
  }, ref: any) => {
    const colors = ["#6586e0", "#cd78d5", "#ff6fa4", "#ff8763", "#ffb624"];
    const parsedData = props.value;
    var data = [];
    var datas = [];
    var xaxis = null;
    var lines = [];
    var units = ["", ""];

    if (props.units !== undefined) {
      if (props.units[0] !== undefined) { // not sure if this will get fooled by strings
        units[0] = props.units[0];
        units[1] = props.units[1];
      } else {
        units[1] = props.units;
      }
    }

    if (parsedData[0][0].length !== undefined) { // we have deep arrays ((x1, y1), (x2, y2), ...)
      for (var ids = 0; ids < parsedData.length; ids++) {
        data = [];
        for (var i = 0; i < parsedData[ids][0].length; i++) {
          data[i] = {x: parsedData[ids][0][i], ["y"+ids.toString()]: parsedData[ids][1][i]};
        }
        if (ids == 0) {
          xaxis = <XAxis xAxisId={"x"} dataKey={"x"} type="number" domain={['auto', 'auto']}><Label value={units[0]} offset={0} position="insideBottom"/></XAxis>;
        }
        lines[ids] = <Line animationDuration={100}
                        key={"ds"+ids.toString()}
                        type="monotone"
                        xAxisId={"x"}
                        dataKey={"y"+ids.toString()}
                        stroke={colors[((ids % colors.length) + colors.length) % colors.length]}
                        strokeWidth={2}
                        dot={false}
                      />;
        for (var j = 0; j < data.length; j++) {
          const sharesX = (element) => element.x == data[j].x;
          const idx = datas.findIndex(sharesX);
          if (idx >= 0) { // this x-value exists already
            datas[idx] = Object.assign(datas[idx], data[j]);
          } else { // no x-value here yet
            datas.push(data[j]);
          }
        }
      }      
    }
    else { // just a single (x, y) set
      for (var i = 0; i < parsedData[0].length; i++) {
        datas[i] = {x: parsedData[0][i], y: parsedData[1][i]};
      }
      xaxis = <XAxis dataKey={"x"} type="number" domain={['auto', 'auto']}><Label value={units[0]} offset={0} position="insideBottom"/></XAxis>;
      lines[0] = <Line animationDuration={100} key={"ds0"} type="monotone" dataKey="y" stroke={colors[0]} strokeWidth={2} dot={false}/>;
    }

    return (
      <div className="component datastream" id={props.fullname}>
        <ComponentLabel ref={ref} {...props}/>
        <ResponsiveContainer width="99%" height="100%">
          <LineChart data={datas}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            {xaxis}
            <YAxis>
              <Label angle={-90} value={units[1]} offset={0} position="insideLeft" style={{textAnchor: 'middle'}}/>
            </YAxis>
            <Tooltip />
            {lines}
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  }
);
const ComponentLineSeries = React.memo(ComponentLineSeriesRef);
