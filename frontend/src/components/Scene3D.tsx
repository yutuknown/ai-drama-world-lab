'use client';

import { useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, PerspectiveCamera } from '@react-three/drei';
import { Object3D as ThreeObject3D } from 'three';
import { Object3D, AgentState } from '@/types';

interface SceneObject3DProps {
  object: Object3D;
}

function SceneObject3D({ object }: SceneObject3DProps) {
  const meshRef = useRef<ThreeObject3D>(null);

  useEffect(() => {
    if (meshRef.current) {
      meshRef.current.position.set(...object.position);
      meshRef.current.rotation.set(...object.rotation);
      meshRef.current.scale.set(...object.scale);
    }
  }, [object]);

  const getGeometry = () => {
    switch (object.type) {
      case 'cube':
        return <boxGeometry args={[1, 1, 1]} />;
      case 'sphere':
        return <sphereGeometry args={[0.5, 32, 32]} />;
      case 'plane':
        return <planeGeometry args={[1, 1]} />;
      default:
        return <boxGeometry args={[1, 1, 1]} />;
    }
  };

  return (
    <mesh ref={meshRef} castShadow receiveShadow>
      {getGeometry()}
      <meshStandardMaterial color={object.color} />
    </mesh>
  );
}

interface AgentMeshProps {
  agent: AgentState;
}

function AgentMesh({ agent }: AgentMeshProps) {
  const meshRef = useRef<ThreeObject3D>(null);
  const targetPosition = useRef<[number, number, number]>(agent.position);

  useEffect(() => {
    targetPosition.current = agent.position;
  }, [agent.position]);

  useFrame(() => {
    if (meshRef.current) {
      // Smooth interpolation
      meshRef.current.position.x += (targetPosition.current[0] - meshRef.current.position.x) * 0.1;
      meshRef.current.position.y = targetPosition.current[1];
      meshRef.current.position.z += (targetPosition.current[2] - meshRef.current.position.z) * 0.1;
      meshRef.current.rotation.y = agent.rotation;
    }
  });

  const getEmotionalColor = () => {
    switch (agent.emotional_state) {
      case 'happy': return '#4ecdc4';
      case 'frustrated': return '#ff6b6b';
      default: return '#45b7d1';
    }
  };

  return (
    <group>
      <mesh ref={meshRef} castShadow>
        <capsuleGeometry args={[0.3, 0.6, 8, 16]} />
        <meshStandardMaterial color={getEmotionalColor()} />
      </mesh>
      {/* Name label */}
      <mesh position={[agent.position[0], agent.position[1] + 1, agent.position[2]]}>
        <planeGeometry args={[1, 0.3]} />
        <meshBasicMaterial color="#ffffff" opacity={0.8} transparent />
      </mesh>
    </group>
  );
}

interface Scene3DProps {
  objects: Object3D[];
  agents: AgentState[];
}

export default function Scene3D({ objects, agents }: Scene3DProps) {
  return (
    <div style={{ width: '100%', height: '100%', background: '#1a1a2e' }}>
      <Canvas shadows>
        <PerspectiveCamera makeDefault position={[10, 10, 10]} />
        <OrbitControls />
        
        {/* Lighting */}
        <ambientLight intensity={0.5} />
        <directionalLight
          position={[10, 10, 5]}
          intensity={1}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        <pointLight position={[-10, 10, -10]} intensity={0.5} />
        
        {/* Grid */}
        <Grid args={[20, 20]} cellColor="#6f6f6f" sectionColor="#9d4b4b" />
        
        {/* Scene objects */}
        {objects.map((obj) => (
          <SceneObject3D key={obj.id} object={obj} />
        ))}
        
        {/* Agents */}
        {agents.map((agent) => (
          <AgentMesh key={agent.id} agent={agent} />
        ))}
      </Canvas>
    </div>
  );
}
