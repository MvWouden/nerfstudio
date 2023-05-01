/* eslint-disable react/jsx-props-no-spreading */
import path from 'path';
import * as React from 'react';

import { Box, Button, Modal, Typography } from '@mui/material';
import { useSelector } from 'react-redux';
import ContentCopyRoundedIcon from '@mui/icons-material/ContentCopyRounded';
import { split_path } from '../../utils';

interface RenderModalProps {
  open: object;
  setOpen: object;
}

export default function RenderModal(props: RenderModalProps) {
  const open = props.open;
  const setOpen = props.setOpen;

  // redux store state
  const config_base_dir = useSelector(
    (state) => state.file_path_info.config_base_dir,
  );

  const export_path = useSelector(
    (state) => state.file_path_info.export_path_name,
  );

  const data_base_dir = useSelector(
    (state) => state.file_path_info.data_base_dir,
  );

  // react state

  const handleClose = () => setOpen(false);

  // Copy the text inside the text field
  const config_filename = `${config_base_dir}${path.sep}config.yml`;
  const camera_path_filename = [data_base_dir, 'camera_paths', `${export_path}.json`].join(path.sep);
  const data_base_dir_leaf = split_path(data_base_dir).pop();
  const render_dir = path.isAbsolute(data_base_dir_leaf) ? data_base_dir_leaf : `renders${path.sep}${data_base_dir_leaf}`;
  const output_path = `${render_dir}${path.sep}${export_path}.mp4`;
  const cmd = `ns-render --load-config ${config_filename} --traj filename --camera-path-filename ${camera_path_filename} --output-path ${output_path}`;

  const text_intro = `To render a full resolution video, run the following command in a terminal.`;

  const handleCopy = () => {
    navigator.clipboard.writeText(cmd);
    handleClose();
  };

  return (
    <div className="RenderModal">
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box className="RenderModal-box">
          <Typography
            id="modal-modal-description"
            component="div"
            sx={{ mt: 2 }}
          >
            <div className="RenderModel-content">
              <h2>Rendering</h2>
              <p>
                {text_intro}
                <br />
                The video will be saved to{' '}
                <code className="RenderModal-inline-code">
                  .{path.sep}{output_path}
                </code>
                .
              </p>

              <div className="RenderModal-code">{cmd}</div>
              <div style={{ textAlign: 'center' }}>
                <Button
                  className="RenderModal-button"
                  variant="outlined"
                  size="small"
                  startIcon={<ContentCopyRoundedIcon />}
                  onClick={handleCopy}
                >
                  Copy Command
                </Button>
              </div>
            </div>
          </Typography>
        </Box>
      </Modal>
    </div>
  );
}
