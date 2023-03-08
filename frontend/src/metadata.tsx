export default interface MetadataProps {
  min?: number;
  max?: number;
  step?: number;
  units?: string;
  doc?: string;
  renderAs?: string;
  displayName?: string;
  isImage?: boolean; // deprecated
  isDataStream?: boolean; // deprecated
  isSlider?: boolean; // deprecated
}