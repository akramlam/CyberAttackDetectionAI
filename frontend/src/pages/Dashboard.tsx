import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
  IconButton,
  useTheme
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Warning as WarningIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon
} from '@mui/icons-material';
import { RealTimeMonitor } from '../components/Dashboard/RealTimeMonitor';
import { SecurityOverview } from '../components/Dashboard/SecurityOverview';
import { SystemHealth } from '../components/Dashboard/SystemHealth';

const StatCard = ({ title, value, icon, color }: any) => (
  <Card>
    <CardContent>
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Box>
          <Typography color="textSecondary" gutterBottom>
            {title}
          </Typography>
          <Typography variant="h4">
            {value}
          </Typography>
        </Box>
        <Box sx={{ color }}>
          {icon}
        </Box>
      </Box>
    </CardContent>
  </Card>
);

export const Dashboard: React.FC = () => {
  const theme = useTheme();

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Dashboard</Typography>
        <IconButton>
          <RefreshIcon />
        </IconButton>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Threat Level"
            value="Low"
            icon={<SecurityIcon sx={{ fontSize: 40 }} />}
            color={theme.palette.success.main}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Active Alerts"
            value="2"
            icon={<WarningIcon sx={{ fontSize: 40 }} />}
            color={theme.palette.warning.main}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Network Load"
            value="65%"
            icon={<SpeedIcon sx={{ fontSize: 40 }} />}
            color={theme.palette.info.main}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="System Health"
            value="Good"
            icon={<SecurityIcon sx={{ fontSize: 40 }} />}
            color={theme.palette.success.main}
          />
        </Grid>

        <Grid item xs={12}>
          <RealTimeMonitor />
        </Grid>

        <Grid item xs={12} md={8}>
          <SecurityOverview />
        </Grid>

        <Grid item xs={12} md={4}>
          <SystemHealth />
        </Grid>
      </Grid>
    </Box>
  );
}; 