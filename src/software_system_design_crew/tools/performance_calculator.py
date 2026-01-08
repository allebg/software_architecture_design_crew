from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class PerformanceCalculatorInput(BaseModel):
    """Input schema for Performance Calculator."""
    user_load: str = Field(..., description="Expected number of concurrent users or requests per second")
    application_type: str = Field(..., description="Type of application (web, mobile, API, etc.)")
    data_size: str = Field(..., description="Expected data volume and growth rate")


class PerformanceCalculator(BaseTool):
    name: str = "Performance Calculator"
    description: str = (
        "Calculates performance metrics and resource requirements for software systems. "
        "Estimates response times, throughput, memory usage, and scaling requirements. "
        "Provides capacity planning recommendations based on expected load."
    )
    args_schema: Type[BaseModel] = PerformanceCalculatorInput

    def _run(self, user_load: str, application_type: str, data_size: str) -> str:
        # Extract numeric values from user input
        import re
        
        # Parse user load
        load_numbers = re.findall(r'\d+', user_load)
        concurrent_users = int(load_numbers[0]) if load_numbers else 1000
        
        # Parse data size
        data_numbers = re.findall(r'\d+', data_size)
        data_volume_gb = int(data_numbers[0]) if data_numbers else 100
        
        # Performance calculations
        requests_per_second = concurrent_users * 2  # Assume 2 requests per user per second
        peak_rps = requests_per_second * 3  # Peak traffic multiplier
        
        # Memory calculations (rough estimates)
        base_memory_mb = 512
        memory_per_user_kb = 2
        total_memory_mb = base_memory_mb + (concurrent_users * memory_per_user_kb / 1024)
        
        # Database calculations
        db_connections = min(concurrent_users // 10, 100)  # Connection pooling
        db_memory_mb = data_volume_gb * 0.25 * 1024  # 25% of data size for caching
        
        # CPU calculations
        cpu_cores = max(2, concurrent_users // 500)  # Rough estimate
        
        # Network bandwidth
        avg_response_size_kb = 50
        bandwidth_mbps = (requests_per_second * avg_response_size_kb * 8) / 1024  # Convert to Mbps
        
        performance_report = f"""
# Performance Analysis Report

## Load Analysis
- **Concurrent Users:** {concurrent_users:,}
- **Average RPS:** {requests_per_second:,}
- **Peak RPS:** {peak_rps:,}
- **Application Type:** {application_type}

## Resource Requirements

### Compute Resources
- **Recommended CPU Cores:** {cpu_cores}
- **Memory Requirement:** {total_memory_mb:.0f} MB ({total_memory_mb/1024:.1f} GB)
- **Peak Memory:** {total_memory_mb * 1.5:.0f} MB ({(total_memory_mb * 1.5)/1024:.1f} GB)

### Database Resources
- **Connection Pool Size:** {db_connections}
- **Database Memory:** {db_memory_mb:.0f} MB ({db_memory_mb/1024:.1f} GB)
- **Data Volume:** {data_volume_gb} GB
- **Recommended Storage:** {data_volume_gb * 2} GB (with growth buffer)

### Network Requirements
- **Bandwidth:** {bandwidth_mbps:.1f} Mbps
- **Peak Bandwidth:** {bandwidth_mbps * 3:.1f} Mbps
- **CDN Recommended:** {'Yes' if bandwidth_mbps > 10 else 'Optional'}

## Performance Targets

### Response Time Targets
- **API Endpoints:** < 200ms (95th percentile)
- **Database Queries:** < 100ms (average)
- **Page Load Time:** < 2 seconds
- **Time to First Byte:** < 500ms

### Throughput Targets
- **Sustained RPS:** {requests_per_second:,}
- **Peak RPS:** {peak_rps:,}
- **Database TPS:** {requests_per_second // 2:,}

## Scaling Recommendations

### Horizontal Scaling
- **Application Servers:** {max(2, concurrent_users // 1000)} instances
- **Load Balancer:** Required for > 1000 users
- **Auto-scaling Triggers:** CPU > 70%, Memory > 80%

### Caching Strategy
- **Application Cache:** Redis/Memcached ({max(1, total_memory_mb // 4):.0f} MB)
- **Database Cache:** {max(512, db_memory_mb // 4):.0f} MB
- **CDN Cache:** Static assets and API responses
- **Cache Hit Ratio Target:** > 80%

### Database Scaling
- **Read Replicas:** {max(1, concurrent_users // 2000)} replicas
- **Connection Pooling:** {db_connections} connections
- **Query Optimization:** Index critical queries
- **Partitioning:** Consider for > 1TB data

## Performance Testing Strategy

### Load Testing Scenarios
1. **Normal Load:** {requests_per_second:,} RPS for 30 minutes
2. **Peak Load:** {peak_rps:,} RPS for 10 minutes  
3. **Stress Test:** {peak_rps * 2:,} RPS until failure
4. **Endurance Test:** {requests_per_second:,} RPS for 24 hours

### Key Metrics to Monitor
- Response time (p50, p95, p99)
- Throughput (RPS)
- Error rate (< 0.1%)
- CPU utilization (< 70%)
- Memory usage (< 80%)
- Database performance
- Cache hit rates

## Capacity Planning

### Growth Projections (12 months)
- **User Growth:** Assume 2x growth
- **Data Growth:** Assume 3x growth  
- **Infrastructure:** Plan for 4x capacity

### Cost Optimization
- Use auto-scaling to handle traffic spikes
- Implement efficient caching to reduce database load
- Optimize database queries and indexes
- Consider serverless for variable workloads

## Risk Mitigation
- **Single Point of Failure:** Eliminate with redundancy
- **Database Bottlenecks:** Implement read replicas and caching
- **Network Latency:** Use CDN and edge locations
- **Memory Leaks:** Implement monitoring and alerts
"""

        return performance_report
