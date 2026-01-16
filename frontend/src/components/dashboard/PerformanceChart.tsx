import { motion } from 'framer-motion';
import {
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Area,
    AreaChart
} from 'recharts';
import { itemVariants } from '../../lib/animations';
import styles from './PerformanceChart.module.css';

interface ChartDataPoint {
    date: string;
    sent: number;
    opened: number;
    clicked?: number;
}

interface PerformanceChartProps {
    data: ChartDataPoint[];
    title?: string;
}

const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
        return (
            <div className={styles.tooltip}>
                <p className={styles.tooltipLabel}>{label}</p>
                {payload.map((entry: any, index: number) => (
                    <p
                        key={index}
                        className={styles.tooltipValue}
                        style={{ color: entry.color }}
                    >
                        {entry.name}: {entry.value.toLocaleString()}
                    </p>
                ))}
            </div>
        );
    }
    return null;
};

export function PerformanceChart({ data, title = 'Campaign Performance' }: PerformanceChartProps) {
    return (
        <motion.div
            className={styles.container}
            variants={itemVariants}
        >
            <div className={styles.header}>
                <h3 className={styles.title}>{title}</h3>
                <div className={styles.legend}>
                    <div className={styles.legendItem}>
                        <span className={`${styles.legendDot} ${styles.sent}`} />
                        <span>Sent</span>
                    </div>
                    <div className={styles.legendItem}>
                        <span className={`${styles.legendDot} ${styles.opened}`} />
                        <span>Opened</span>
                    </div>
                </div>
            </div>

            <div className={styles.chartWrapper}>
                <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                        <defs>
                            <linearGradient id="sentGradient" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="openedGradient" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid
                            strokeDasharray="3 3"
                            stroke="rgba(148, 163, 184, 0.1)"
                            vertical={false}
                        />
                        <XAxis
                            dataKey="date"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#64748b', fontSize: 12 }}
                            dy={10}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#64748b', fontSize: 12 }}
                            dx={-10}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Area
                            type="monotone"
                            dataKey="sent"
                            name="Sent"
                            stroke="#3b82f6"
                            strokeWidth={2}
                            fill="url(#sentGradient)"
                        />
                        <Area
                            type="monotone"
                            dataKey="opened"
                            name="Opened"
                            stroke="#10b981"
                            strokeWidth={2}
                            fill="url(#openedGradient)"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </motion.div>
    );
}
