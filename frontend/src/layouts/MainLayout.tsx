import React from 'react';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  IconButton,
  ListItem,
  ListItemIcon,
  ListItemText,
  useTheme,
  styled
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Security as SecurityIcon,
  Timeline as TimelineIcon,
  Settings as SettingsIcon,
  Notifications as NotificationsIcon,
  ExitToApp as LogoutIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const drawerWidth = 240;

const Root = styled('div')({
  display: 'flex',
});

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  zIndex: theme.zIndex.drawer + 1,
}));

const StyledDrawer = styled(Drawer)(({ theme }) => ({
  width: drawerWidth,
  flexShrink: 0,
  '& .MuiDrawer-paper': {
    width: drawerWidth,
    boxSizing: 'border-box',
  },
}));

interface MainLayoutProps {
  children: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const theme = useTheme();
  const navigate = useNavigate();

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
    { text: 'Security Events', icon: <SecurityIcon />, path: '/security' },
    { text: 'Network Analysis', icon: <TimelineIcon />, path: '/network' },
    { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
  ];

  return (
    <Root>
      <StyledAppBar position="fixed">
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            sx={{ marginRight: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Cyber Attack Detection System
          </Typography>
          <IconButton color="inherit">
            <NotificationsIcon />
          </IconButton>
          <IconButton color="inherit">
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </StyledAppBar>
      <StyledDrawer variant="permanent">
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <ListItem 
                button 
                key={item.text}
                onClick={() => navigate(item.path)}
              >
                <ListItemIcon>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
          </List>
        </Box>
      </StyledDrawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {children}
      </Box>
    </Root>
  );
}; 