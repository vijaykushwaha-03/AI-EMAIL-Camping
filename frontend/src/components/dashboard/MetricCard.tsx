import { useEffect, useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { counterVariants } from '../../lib/animations';
import styles from './MetricCard.module.css';

interface MetricCardProps {
    title: string;
    value: number;
    suffix?: string;
    prefix?: string;
    change?: number;
    changeLabel?: string;
    icon: React.ReactNode;
    color?: 'blue' | 'green' | 'purple' | 'orange';
}

export function MetricCard({
    title,
    value,
    suffix = '',
    prefix = '',
    change,
    changeLabel = 'vs last month',
    icon,
    color = 'blue',
}: MetricCardProps) {
    const [displayValue, setDisplayValue] = useState(0);
    const hasAnimated = useRef(false);

    // Animate counter on mount
    useEffect(() => {
        if (hasAnimated.current) return;
        hasAnimated.current = true;

        const duration = 1000;
        const steps = 60;
        const increment = value / steps;
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= value) {
                setDisplayValue(value);
                clearInterval(timer);
            } else {
                setDisplayValue(Math.floor(current));
            }
        }, duration / steps);

        return () => clearInterval(timer);
    }, [value]);

    const isPositive = change && change > 0;
    const TrendIcon = isPositive ? TrendingUp : TrendingDown;

    return (
        <motion.div
            className={`${styles.card} ${styles[color]}`}
            variants={counterVariants}
            whileHover={{ y: -4, transition: { duration: 0.2 } }}
        >
            <div className={styles.header}>
                <span className={styles.title}>{title}</span>
                <div className={styles.iconWrapper}>
                    {icon}
                </div>
            </div>

            <div className={styles.valueWrapper}>
                <span className={styles.value}>
                    {prefix}
                    {displayValue.toLocaleString()}
                    {suffix}
                </span>
            </div>

            {change !== undefined && (
                <div className={`${styles.change} ${isPositive ? styles.positive : styles.negative}`}>
                    <TrendIcon size={14} />
                    <span>{Math.abs(change)}%</span>
                    <span className={styles.changeLabel}>{changeLabel}</span>
                </div>
            )}

            {/* Gradient overlay */}
            <div className={styles.gradient} />
        </motion.div>
    );
}
