import path from "path";

export function split_path(path_str) {
  return path_str.split(path.sep).filter((x) => x.length > 0);
}
