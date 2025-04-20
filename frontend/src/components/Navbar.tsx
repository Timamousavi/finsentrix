import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import LanguageSelector from './LanguageSelector';

const Navbar: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          FinSentrix
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            color="inherit"
            component={RouterLink}
            to="/"
          >
            Dashboard
          </Button>
          <Button
            color="inherit"
            component={RouterLink}
            to="/market-analysis"
          >
            Market Analysis
          </Button>
          <Button
            color="inherit"
            component={RouterLink}
            to="/settings"
          >
            Settings
          </Button>
          <LanguageSelector />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 