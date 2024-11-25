import React, { useEffect, useState, useRef } from 'react';
import { Box, Card, CardContent, Typography, Grid } from '@mui/material';
import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    AreaChart,
    Area
} from 'recharts';
import * as d3 from 'd3';
import { trafficService, TrafficData } from '../../services/trafficService';

interface PacketData {
    timestamp: Date;
    source_ip: string;
    destination_ip: string;
    protocol: string;
    size: number;
    type: string;
}

interface NetworkNode {
    id: string;
    type: 'source' | 'destination';
    connections: number;
}

interface NetworkLink {
    source: string;
    target: string;
    value: number;
    protocol: string;
}

export const TrafficVisualizer: React.FC = () => {
    const [packetData, setPacketData] = useState<PacketData[]>([]);
    const [nodes, setNodes] = useState<NetworkNode[]>([]);
    const [links, setLinks] = useState<NetworkLink[]>([]);
    const svgRef = useRef<SVGSVGElement>(null);

    useEffect(() => {
        const unsubscribe = trafficService.addListener((data) => {
            setPacketData(prev => [...prev, data].slice(-100)); // Keep last 100 packets

            // Update nodes and links
            const sourceNode = { id: data.source_ip, type: 'source', connections: 1 };
            const targetNode = { id: data.destination_ip, type: 'destination', connections: 1 };
            
            setNodes(prev => {
                const existingNodes = prev.filter(n => 
                    n.id !== data.source_ip && n.id !== data.destination_ip
                );
                return [...existingNodes, sourceNode, targetNode];
            });

            setLinks(prev => {
                const newLink = {
                    source: data.source_ip,
                    target: data.destination_ip,
                    value: data.size,
                    protocol: data.protocol
                };
                return [...prev, newLink].slice(-50); // Keep last 50 connections
            });
        });

        return () => unsubscribe();
    }, []);

    useEffect(() => {
        const width = 800;
        const height = 600;

        const simulation = d3.forceSimulation()
            .force('link', d3.forceLink().id((d: any) => d.id))
            .force('charge', d3.forceManyBody().strength(-100))
            .force('center', d3.forceCenter(width / 2, height / 2));

        const svg = d3.select(svgRef.current)
            .attr('width', width)
            .attr('height', height);

        // Clear previous content
        svg.selectAll('*').remove();

        const link = svg.append('g')
            .selectAll('line')
            .data(links)
            .enter()
            .append('line')
            .attr('stroke', '#999')
            .attr('stroke-opacity', 0.6)
            .attr('stroke-width', (d) => Math.sqrt(d.value));

        const node = svg.append('g')
            .selectAll('circle')
            .data(nodes)
            .enter()
            .append('circle')
            .attr('r', 5)
            .attr('fill', (d) => d.type === 'source' ? '#ff7f0e' : '#1f77b4')
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended) as any);

        node.append('title')
            .text((d) => d.id);

        simulation
            .nodes(nodes as any)
            .on('tick', ticked);

        (simulation.force('link') as d3.ForceLink<any, any>)
            .links(links);

        function ticked() {
            link
                .attr('x1', (d: any) => d.source.x)
                .attr('y1', (d: any) => d.source.y)
                .attr('x2', (d: any) => d.target.x)
                .attr('y2', (d: any) => d.target.y);

            node
                .attr('cx', (d: any) => d.x)
                .attr('cy', (d: any) => d.y);
        }

        function dragstarted(event: any) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event: any) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event: any) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }
    }, [nodes, links]);

    return (
        <Grid container spacing={3}>
            <Grid item xs={12}>
                <Card>
                    <CardContent>
                        <Typography variant="h6" gutterBottom>
                            Network Traffic Flow
                        </Typography>
                        <Box sx={{ height: 600 }}>
                            <svg ref={svgRef}></svg>
                        </Box>
                    </CardContent>
                </Card>
            </Grid>

            <Grid item xs={12} md={6}>
                <Card>
                    <CardContent>
                        <Typography variant="h6" gutterBottom>
                            Packet Rate Over Time
                        </Typography>
                        <ResponsiveContainer width="100%" height={300}>
                            <AreaChart data={packetData.slice(-50)}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis 
                                    dataKey="timestamp" 
                                    tickFormatter={(time) => new Date(time).toLocaleTimeString()} 
                                />
                                <YAxis />
                                <Tooltip 
                                    labelFormatter={(label) => new Date(label).toLocaleString()}
                                />
                                <Area 
                                    type="monotone" 
                                    dataKey="size" 
                                    stroke="#8884d8" 
                                    fill="#8884d8" 
                                    fillOpacity={0.3}
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>
            </Grid>

            <Grid item xs={12} md={6}>
                <Card>
                    <CardContent>
                        <Typography variant="h6" gutterBottom>
                            Protocol Distribution
                        </Typography>
                        <ResponsiveContainer width="100%" height={300}>
                            <LineChart data={packetData.slice(-50)}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis 
                                    dataKey="timestamp" 
                                    tickFormatter={(time) => new Date(time).toLocaleTimeString()} 
                                />
                                <YAxis />
                                <Tooltip 
                                    labelFormatter={(label) => new Date(label).toLocaleString()}
                                />
                                <Line 
                                    type="monotone" 
                                    dataKey="size" 
                                    stroke="#82ca9d" 
                                    name="Packet Size" 
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
}; 